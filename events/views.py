from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Announcement, Event, RSVP


def announcements(request):
    announcements_list = Announcement.objects.filter(is_active=True)
    paginator = Paginator(announcements_list, 10)
    page_number = request.GET.get('page')
    announcements = paginator.get_page(page_number)
    
    context = {
        'announcements': announcements,
    }
    return render(request, 'events/announcements.html', context)


def events(request):
    upcoming_events = Event.objects.filter(
        is_active=True,
        event_date__gte=timezone.now()
    )
    past_events = Event.objects.filter(
        is_active=True,
        event_date__lt=timezone.now()
    )[:5]  # Show only recent past events
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'events/events.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    user_rsvp = None
    
    if request.user.is_authenticated:
        try:
            user_rsvp = RSVP.objects.get(event=event, user=request.user)
        except RSVP.DoesNotExist:
            pass
    
    context = {
        'event': event,
        'user_rsvp': user_rsvp,
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['attending', 'not_attending', 'maybe']:
            rsvp, created = RSVP.objects.get_or_create(
                event=event,
                user=request.user,
                defaults={'status': status}
            )
            if not created:
                rsvp.status = status
                rsvp.save()
            
            messages.success(request, f'Your RSVP has been updated to "{status}".')
        else:
            messages.error(request, 'Invalid RSVP status.')
    
    return redirect('events:event_detail', event_id=event_id)
