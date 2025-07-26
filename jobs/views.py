from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import JobPosting, JobCategory, JobApplication, SavedJob


def job_board(request):
    jobs = JobPosting.objects.filter(is_approved=True, is_active=True)
    
    # Filters
    category_filter = request.GET.get('category')
    job_type_filter = request.GET.get('job_type')
    location_filter = request.GET.get('location')
    search_query = request.GET.get('search')
    
    if category_filter:
        jobs = jobs.filter(category_id=category_filter)
    
    if job_type_filter:
        jobs = jobs.filter(job_type=job_type_filter)
    
    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)
    
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(jobs, 12)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)
    
    categories = JobCategory.objects.all()
    job_types = JobPosting.JOB_TYPES
    
    context = {
        'jobs': jobs,
        'categories': categories,
        'job_types': job_types,
        'current_category': category_filter,
        'current_job_type': job_type_filter,
        'current_location': location_filter,
        'search_query': search_query,
    }
    return render(request, 'jobs/job_board.html', context)


def job_detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, is_approved=True, is_active=True)
    job.increment_views()
    
    user_applied = False
    user_saved = False
    
    if request.user.is_authenticated:
        user_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
        user_saved = SavedJob.objects.filter(job=job, user=request.user).exists()
    
    context = {
        'job': job,
        'user_applied': user_applied,
        'user_saved': user_saved,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def post_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        experience_level = request.POST.get('experience_level')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        salary_range = request.POST.get('salary_range')
        application_url = request.POST.get('application_url')
        contact_email = request.POST.get('contact_email')
        
        if all([title, company, location, job_type, category_id, description, requirements]):
            category = get_object_or_404(JobCategory, id=category_id)
            JobPosting.objects.create(
                title=title,
                company=company,
                location=location,
                job_type=job_type,
                experience_level=experience_level,
                category=category,
                description=description,
                requirements=requirements,
                salary_range=salary_range,
                application_url=application_url,
                contact_email=contact_email,
                posted_by=request.user
            )
            messages.success(request, 'Your job posting has been submitted for approval.')
            return redirect('jobs:job_board')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    categories = JobCategory.objects.all()
    job_types = JobPosting.JOB_TYPES
    experience_levels = JobPosting.EXPERIENCE_LEVELS
    
    context = {
        'categories': categories,
        'job_types': job_types,
        'experience_levels': experience_levels,
    }
    return render(request, 'jobs/post_job.html', context)


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, is_approved=True, is_active=True)
    
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', job_id=job_id)
    
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')
        resume = request.FILES.get('resume')
        
        JobApplication.objects.create(
            job=job,
            applicant=request.user,
            cover_letter=cover_letter,
            resume=resume
        )
        messages.success(request, 'Your application has been submitted successfully.')
        return redirect('jobs:job_detail', job_id=job_id)
    
    context = {'job': job}
    return render(request, 'jobs/apply_job.html', context)


@login_required
def save_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(JobPosting, id=job_id, is_approved=True, is_active=True)
        saved_job, created = SavedJob.objects.get_or_create(job=job, user=request.user)
        
        if not created:
            saved_job.delete()
            saved = False
        else:
            saved = True
        
        return JsonResponse({
            'status': 'success',
            'saved': saved,
            'message': 'Job saved!' if saved else 'Job removed from saved!'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(applicant=request.user)
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    applications = paginator.get_page(page_number)
    
    context = {'applications': applications}
    return render(request, 'jobs/my_applications.html', context)


@login_required
def saved_jobs(request):
    saved_jobs_list = SavedJob.objects.filter(user=request.user)
    paginator = Paginator(saved_jobs_list, 10)
    page_number = request.GET.get('page')
    saved_jobs = paginator.get_page(page_number)
    
    context = {'saved_jobs': saved_jobs}
    return render(request, 'jobs/saved_jobs.html', context)
