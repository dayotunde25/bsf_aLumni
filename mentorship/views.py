from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import MentorProfile, MentorshipRequest, Mentorship, MentorshipSession, MentorshipFeedback


def mentors(request):
    mentors_list = MentorProfile.objects.filter(is_active=True)
    
    # Filters
    expertise_filter = request.GET.get('expertise')
    if expertise_filter:
        mentors_list = mentors_list.filter(expertise_areas__icontains=expertise_filter)
    
    paginator = Paginator(mentors_list, 12)
    page_number = request.GET.get('page')
    mentors = paginator.get_page(page_number)
    
    expertise_areas = MentorProfile.EXPERTISE_AREAS
    
    context = {
        'mentors': mentors,
        'expertise_areas': expertise_areas,
        'current_expertise': expertise_filter,
    }
    return render(request, 'mentorship/mentors.html', context)


def mentor_detail(request, mentor_id):
    mentor = get_object_or_404(MentorProfile, id=mentor_id, is_active=True)
    
    # Check if user already has a request or mentorship with this mentor
    existing_request = None
    existing_mentorship = None
    
    if request.user.is_authenticated:
        existing_request = MentorshipRequest.objects.filter(
            mentee=request.user,
            mentor=mentor,
            status__in=['pending', 'accepted']
        ).first()
        
        existing_mentorship = Mentorship.objects.filter(
            mentor=mentor,
            mentee=request.user,
            status='active'
        ).first()
    
    context = {
        'mentor': mentor,
        'existing_request': existing_request,
        'existing_mentorship': existing_mentorship,
    }
    return render(request, 'mentorship/mentor_detail.html', context)


@login_required
def become_mentor(request):
    # Check if user already has a mentor profile
    try:
        mentor_profile = request.user.mentor_profile
        return redirect('mentorship:mentor_dashboard')
    except MentorProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        bio = request.POST.get('bio')
        expertise_areas = request.POST.getlist('expertise_areas')
        years_of_experience = request.POST.get('years_of_experience')
        availability = request.POST.get('availability')
        max_mentees = request.POST.get('max_mentees')
        
        if all([bio, expertise_areas, years_of_experience, availability, max_mentees]):
            mentor_profile = MentorProfile.objects.create(
                user=request.user,
                bio=bio,
                years_of_experience=int(years_of_experience),
                availability=availability,
                max_mentees=int(max_mentees)
            )
            mentor_profile.set_expertise_areas(expertise_areas)
            messages.success(request, 'Your mentor profile has been created successfully!')
            return redirect('mentorship:mentor_dashboard')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    expertise_areas = MentorProfile.EXPERTISE_AREAS
    context = {'expertise_areas': expertise_areas}
    return render(request, 'mentorship/become_mentor.html', context)


@login_required
def request_mentorship(request, mentor_id):
    mentor = get_object_or_404(MentorProfile, id=mentor_id, is_active=True)
    
    # Check if user already has a request or mentorship
    if MentorshipRequest.objects.filter(
        mentee=request.user,
        mentor=mentor,
        status__in=['pending', 'accepted']
    ).exists():
        messages.warning(request, 'You already have a pending or accepted request with this mentor.')
        return redirect('mentorship:mentor_detail', mentor_id=mentor_id)
    
    if Mentorship.objects.filter(
        mentor=mentor,
        mentee=request.user,
        status='active'
    ).exists():
        messages.warning(request, 'You already have an active mentorship with this mentor.')
        return redirect('mentorship:mentor_detail', mentor_id=mentor_id)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        area_of_interest = request.POST.get('area_of_interest')
        
        if message and area_of_interest:
            MentorshipRequest.objects.create(
                mentee=request.user,
                mentor=mentor,
                message=message,
                area_of_interest=area_of_interest
            )
            messages.success(request, 'Your mentorship request has been sent!')
            return redirect('mentorship:mentor_detail', mentor_id=mentor_id)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    expertise_areas = MentorProfile.EXPERTISE_AREAS
    context = {
        'mentor': mentor,
        'expertise_areas': expertise_areas,
    }
    return render(request, 'mentorship/request_mentorship.html', context)


@login_required
def mentor_dashboard(request):
    try:
        mentor_profile = request.user.mentor_profile
    except MentorProfile.DoesNotExist:
        return redirect('mentorship:become_mentor')
    
    pending_requests = MentorshipRequest.objects.filter(
        mentor=mentor_profile,
        status='pending'
    )
    
    active_mentorships = Mentorship.objects.filter(
        mentor=mentor_profile,
        status='active'
    )
    
    context = {
        'mentor_profile': mentor_profile,
        'pending_requests': pending_requests,
        'active_mentorships': active_mentorships,
    }
    return render(request, 'mentorship/mentor_dashboard.html', context)


@login_required
def mentee_dashboard(request):
    my_requests = MentorshipRequest.objects.filter(mentee=request.user)
    my_mentorships = Mentorship.objects.filter(mentee=request.user, status='active')
    
    context = {
        'my_requests': my_requests,
        'my_mentorships': my_mentorships,
    }
    return render(request, 'mentorship/mentee_dashboard.html', context)


@login_required
def respond_to_request(request, request_id):
    mentorship_request = get_object_or_404(
        MentorshipRequest,
        id=request_id,
        mentor__user=request.user,
        status='pending'
    )
    
    if request.method == 'POST':
        action = request.POST.get('action')
        response_message = request.POST.get('response_message', '')
        
        if action == 'accept':
            mentorship_request.status = 'accepted'
            mentorship_request.response_message = response_message
            mentorship_request.save()
            
            # Create mentorship
            Mentorship.objects.create(
                mentor=mentorship_request.mentor,
                mentee=mentorship_request.mentee,
                area_of_focus=mentorship_request.area_of_interest,
                goals=mentorship_request.message
            )
            
            messages.success(request, 'Mentorship request accepted!')
        
        elif action == 'decline':
            mentorship_request.status = 'declined'
            mentorship_request.response_message = response_message
            mentorship_request.save()
            
            messages.success(request, 'Mentorship request declined.')
        
        return redirect('mentorship:mentor_dashboard')
    
    context = {'mentorship_request': mentorship_request}
    return render(request, 'mentorship/respond_to_request.html', context)
