from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import PrayerRequest, Prayer, PrayerComment, Testimony, TestimonyLike


def prayer_wall(request):
    prayer_requests = PrayerRequest.objects.filter(is_approved=True)
    category_filter = request.GET.get('category')
    
    if category_filter:
        prayer_requests = prayer_requests.filter(category=category_filter)
    
    paginator = Paginator(prayer_requests, 10)
    page_number = request.GET.get('page')
    prayer_requests = paginator.get_page(page_number)
    
    categories = PrayerRequest.CATEGORY_CHOICES
    
    context = {
        'prayer_requests': prayer_requests,
        'categories': categories,
        'current_category': category_filter,
    }
    return render(request, 'prayer/prayer_wall.html', context)


def prayer_detail(request, prayer_id):
    prayer_request = get_object_or_404(PrayerRequest, id=prayer_id, is_approved=True)
    comments = prayer_request.comments.all()
    user_prayed = False
    
    if request.user.is_authenticated:
        user_prayed = Prayer.objects.filter(prayer_request=prayer_request, user=request.user).exists()
    
    context = {
        'prayer_request': prayer_request,
        'comments': comments,
        'user_prayed': user_prayed,
    }
    return render(request, 'prayer/prayer_detail.html', context)


@login_required
def add_prayer_request(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        if title and description:
            PrayerRequest.objects.create(
                title=title,
                description=description,
                category=category,
                requested_by=request.user,
                is_anonymous=is_anonymous
            )
            messages.success(request, 'Your prayer request has been submitted for approval.')
            return redirect('prayer:prayer_wall')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    categories = PrayerRequest.CATEGORY_CHOICES
    context = {'categories': categories}
    return render(request, 'prayer/add_prayer_request.html', context)


@login_required
def pray_for_request(request, prayer_id):
    if request.method == 'POST':
        prayer_request = get_object_or_404(PrayerRequest, id=prayer_id, is_approved=True)
        prayer, created = Prayer.objects.get_or_create(
            prayer_request=prayer_request,
            user=request.user
        )
        
        if created:
            return JsonResponse({'status': 'success', 'message': 'You are now praying for this request.'})
        else:
            prayer.delete()
            return JsonResponse({'status': 'success', 'message': 'Prayer removed.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def testimonies(request):
    testimonies_list = Testimony.objects.filter(is_approved=True)
    paginator = Paginator(testimonies_list, 10)
    page_number = request.GET.get('page')
    testimonies = paginator.get_page(page_number)
    
    context = {'testimonies': testimonies}
    return render(request, 'prayer/testimonies.html', context)


@login_required
def add_testimony(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        if title and content:
            Testimony.objects.create(
                title=title,
                content=content,
                author=request.user,
                is_anonymous=is_anonymous
            )
            messages.success(request, 'Your testimony has been submitted for approval.')
            return redirect('prayer:testimonies')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'prayer/add_testimony.html')


@login_required
def like_testimony(request, testimony_id):
    if request.method == 'POST':
        testimony = get_object_or_404(Testimony, id=testimony_id, is_approved=True)
        like, created = TestimonyLike.objects.get_or_create(
            testimony=testimony,
            user=request.user
        )
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        like_count = testimony.likes.count()
        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'like_count': like_count
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
