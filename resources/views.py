from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, Http404
from django.db.models import Q, Avg
from .models import Resource, ResourceCategory, ResourceDownload, ResourceRating, ResourceBookmark


def resource_hub(request):
    resources = Resource.objects.filter(is_approved=True)
    
    # Filters
    category_filter = request.GET.get('category')
    resource_type_filter = request.GET.get('resource_type')
    search_query = request.GET.get('search')
    
    if category_filter:
        resources = resources.filter(category_id=category_filter)
    
    if resource_type_filter:
        resources = resources.filter(resource_type=resource_type_filter)
    
    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    paginator = Paginator(resources, 12)
    page_number = request.GET.get('page')
    resources = paginator.get_page(page_number)
    
    categories = ResourceCategory.objects.all()
    resource_types = Resource.RESOURCE_TYPES
    featured_resources = Resource.objects.filter(is_approved=True, is_featured=True)[:6]
    
    context = {
        'resources': resources,
        'categories': categories,
        'resource_types': resource_types,
        'featured_resources': featured_resources,
        'current_category': category_filter,
        'current_resource_type': resource_type_filter,
        'search_query': search_query,
    }
    return render(request, 'resources/resource_hub.html', context)


def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id, is_approved=True)
    
    # Get ratings and calculate average
    ratings = resource.ratings.all()
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    
    user_rating = None
    user_bookmarked = False
    
    if request.user.is_authenticated:
        try:
            user_rating = ResourceRating.objects.get(resource=resource, user=request.user)
        except ResourceRating.DoesNotExist:
            pass
        
        user_bookmarked = ResourceBookmark.objects.filter(
            resource=resource, user=request.user
        ).exists()
    
    # Related resources
    related_resources = Resource.objects.filter(
        category=resource.category,
        is_approved=True
    ).exclude(id=resource.id)[:4]
    
    context = {
        'resource': resource,
        'ratings': ratings,
        'avg_rating': round(avg_rating, 1),
        'user_rating': user_rating,
        'user_bookmarked': user_bookmarked,
        'related_resources': related_resources,
    }
    return render(request, 'resources/resource_detail.html', context)


@login_required
def upload_resource(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        resource_type = request.POST.get('resource_type')
        category_id = request.POST.get('category')
        author = request.POST.get('author')
        file = request.FILES.get('file')
        external_url = request.POST.get('external_url')
        tags = request.POST.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        if all([title, description, resource_type, category_id]):
            category = get_object_or_404(ResourceCategory, id=category_id)
            
            # Validate file or URL based on resource type
            if resource_type == 'link' and not external_url:
                messages.error(request, 'External URL is required for link resources.')
            elif resource_type != 'link' and not file:
                messages.error(request, 'File is required for this resource type.')
            else:
                resource = Resource.objects.create(
                    title=title,
                    description=description,
                    resource_type=resource_type,
                    category=category,
                    author=author,
                    file=file if resource_type != 'link' else None,
                    external_url=external_url if resource_type == 'link' else None,
                    uploaded_by=request.user
                )
                resource.set_tags(tags)
                messages.success(request, 'Your resource has been submitted for approval.')
                return redirect('resources:resource_hub')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    categories = ResourceCategory.objects.all()
    resource_types = Resource.RESOURCE_TYPES
    
    context = {
        'categories': categories,
        'resource_types': resource_types,
    }
    return render(request, 'resources/upload_resource.html', context)


@login_required
def download_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id, is_approved=True)
    
    if resource.resource_type == 'link':
        # Redirect to external URL
        resource.increment_downloads()
        ResourceDownload.objects.create(
            resource=resource,
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return redirect(resource.external_url)
    
    if not resource.file:
        raise Http404("File not found")
    
    # Record download
    resource.increment_downloads()
    ResourceDownload.objects.create(
        resource=resource,
        user=request.user,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    # Serve file
    response = HttpResponse(resource.file.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{resource.file.name}"'
    return response


@login_required
def rate_resource(request, resource_id):
    if request.method == 'POST':
        resource = get_object_or_404(Resource, id=resource_id, is_approved=True)
        rating_value = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        if rating_value and 1 <= int(rating_value) <= 5:
            rating, created = ResourceRating.objects.get_or_create(
                resource=resource,
                user=request.user,
                defaults={'rating': int(rating_value), 'comment': comment}
            )
            
            if not created:
                rating.rating = int(rating_value)
                rating.comment = comment
                rating.save()
            
            # Calculate new average
            avg_rating = resource.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
            
            return JsonResponse({
                'status': 'success',
                'message': 'Rating submitted successfully!',
                'avg_rating': round(avg_rating, 1)
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid rating value.'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


@login_required
def bookmark_resource(request, resource_id):
    if request.method == 'POST':
        resource = get_object_or_404(Resource, id=resource_id, is_approved=True)
        bookmark, created = ResourceBookmark.objects.get_or_create(
            resource=resource,
            user=request.user
        )
        
        if not created:
            bookmark.delete()
            bookmarked = False
        else:
            bookmarked = True
        
        return JsonResponse({
            'status': 'success',
            'bookmarked': bookmarked,
            'message': 'Resource bookmarked!' if bookmarked else 'Bookmark removed!'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


@login_required
def my_bookmarks(request):
    bookmarks = ResourceBookmark.objects.filter(user=request.user)
    paginator = Paginator(bookmarks, 12)
    page_number = request.GET.get('page')
    bookmarks = paginator.get_page(page_number)
    
    context = {'bookmarks': bookmarks}
    return render(request, 'resources/my_bookmarks.html', context)
