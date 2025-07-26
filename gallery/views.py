from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import MediaItem, Event


def index(request):
    media_items = MediaItem.objects.filter(is_approved=True)
    
    # Filters
    event_filter = request.GET.get('event')
    media_type_filter = request.GET.get('media_type')
    session_filter = request.GET.get('session')
    
    if event_filter:
        media_items = media_items.filter(event_id=event_filter)
    
    if media_type_filter:
        media_items = media_items.filter(media_type=media_type_filter)
    
    if session_filter:
        media_items = media_items.filter(session=session_filter)
    
    paginator = Paginator(media_items, 12)
    page_number = request.GET.get('page')
    media_items = paginator.get_page(page_number)
    
    events = Event.objects.all()
    media_types = MediaItem.MEDIA_TYPES
    sessions = MediaItem.objects.values_list('session', flat=True).distinct()
    
    context = {
        'media_items': media_items,
        'events': events,
        'media_types': media_types,
        'sessions': sessions,
        'current_event': event_filter,
        'current_media_type': media_type_filter,
        'current_session': session_filter,
    }
    return render(request, 'gallery/index.html', context)


def media_detail(request, media_id):
    media_item = get_object_or_404(MediaItem, id=media_id, is_approved=True)
    
    # Get related media from the same event
    related_media = MediaItem.objects.filter(
        event=media_item.event,
        is_approved=True
    ).exclude(id=media_item.id)[:6]
    
    context = {
        'media_item': media_item,
        'related_media': related_media,
    }
    return render(request, 'gallery/media_detail.html', context)


@login_required
def upload_media(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        media_type = request.POST.get('media_type')
        event_id = request.POST.get('event')
        session = request.POST.get('session')
        file = request.FILES.get('file')
        
        if all([title, media_type, session, file]):
            event = None
            if event_id:
                event = get_object_or_404(Event, id=event_id)
            
            MediaItem.objects.create(
                title=title,
                description=description,
                media_type=media_type,
                file=file,
                event=event,
                session=session,
                uploaded_by=request.user
            )
            messages.success(request, 'Your media has been uploaded and is pending approval.')
            return redirect('gallery:index')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    events = Event.objects.all()
    media_types = MediaItem.MEDIA_TYPES
    
    context = {
        'events': events,
        'media_types': media_types,
    }
    return render(request, 'gallery/upload_media.html', context)


def events(request):
    events_list = Event.objects.all()
    paginator = Paginator(events_list, 12)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    
    context = {'events': events}
    return render(request, 'gallery/events.html', context)


def event_gallery(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    media_items = MediaItem.objects.filter(event=event, is_approved=True)
    
    paginator = Paginator(media_items, 12)
    page_number = request.GET.get('page')
    media_items = paginator.get_page(page_number)
    
    context = {
        'event': event,
        'media_items': media_items,
    }
    return render(request, 'gallery/event_gallery.html', context)
