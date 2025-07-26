from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import HistoryEvent, HistoryCategory, ExecutiveHistory, Milestone, HistoryContribution


def fellowship_history(request):
    # Get featured milestones
    featured_milestones = Milestone.objects.filter(is_approved=True, is_featured=True)[:6]
    
    # Get recent history events
    recent_events = HistoryEvent.objects.filter(is_approved=True)[:8]
    
    # Get categories for filtering
    categories = HistoryCategory.objects.all()
    
    context = {
        'featured_milestones': featured_milestones,
        'recent_events': recent_events,
        'categories': categories,
    }
    return render(request, 'history/fellowship_history.html', context)


def timeline(request):
    # Get all approved events and milestones, ordered by date
    events = HistoryEvent.objects.filter(is_approved=True)
    milestones = Milestone.objects.filter(is_approved=True)
    
    # Filter by category if specified
    category_filter = request.GET.get('category')
    if category_filter:
        events = events.filter(category_id=category_filter)
    
    # Filter by year if specified
    year_filter = request.GET.get('year')
    if year_filter:
        events = events.filter(event_date__year=year_filter)
        milestones = milestones.filter(date__year=year_filter)
    
    # Combine and sort by date
    timeline_items = []
    
    for event in events:
        timeline_items.append({
            'type': 'event',
            'date': event.event_date,
            'title': event.title,
            'description': event.description,
            'category': event.category,
            'image': event.image,
            'location': event.location,
        })
    
    for milestone in milestones:
        timeline_items.append({
            'type': 'milestone',
            'date': milestone.date,
            'title': milestone.title,
            'description': milestone.description,
            'milestone_type': milestone.milestone_type,
            'image': milestone.image,
        })
    
    # Sort by date
    timeline_items.sort(key=lambda x: x['date'])
    
    # Get available years for filtering
    all_years = set()
    for item in timeline_items:
        all_years.add(item['date'].year)
    available_years = sorted(all_years, reverse=True)
    
    categories = HistoryCategory.objects.all()
    
    context = {
        'timeline_items': timeline_items,
        'categories': categories,
        'available_years': available_years,
        'current_category': category_filter,
        'current_year': year_filter,
    }
    return render(request, 'history/timeline.html', context)


def executives(request):
    executives_list = ExecutiveHistory.objects.filter(is_approved=True)
    
    # Filter by session if specified
    session_filter = request.GET.get('session')
    if session_filter:
        executives_list = executives_list.filter(session=session_filter)
    
    # Filter by position if specified
    position_filter = request.GET.get('position')
    if position_filter:
        executives_list = executives_list.filter(position=position_filter)
    
    paginator = Paginator(executives_list, 12)
    page_number = request.GET.get('page')
    executives = paginator.get_page(page_number)
    
    # Get available sessions and positions for filtering
    available_sessions = ExecutiveHistory.objects.filter(is_approved=True).values_list('session', flat=True).distinct()
    positions = ExecutiveHistory.POSITION_CHOICES
    
    context = {
        'executives': executives,
        'available_sessions': sorted(available_sessions, reverse=True),
        'positions': positions,
        'current_session': session_filter,
        'current_position': position_filter,
    }
    return render(request, 'history/executives.html', context)


def executive_detail(request, executive_id):
    executive = get_object_or_404(ExecutiveHistory, id=executive_id, is_approved=True)
    
    # Get other executives from the same session
    session_executives = ExecutiveHistory.objects.filter(
        session=executive.session,
        is_approved=True
    ).exclude(id=executive.id)
    
    context = {
        'executive': executive,
        'session_executives': session_executives,
    }
    return render(request, 'history/executive_detail.html', context)


def milestones(request):
    milestones_list = Milestone.objects.filter(is_approved=True)
    
    # Filter by milestone type if specified
    type_filter = request.GET.get('type')
    if type_filter:
        milestones_list = milestones_list.filter(milestone_type=type_filter)
    
    paginator = Paginator(milestones_list, 12)
    page_number = request.GET.get('page')
    milestones = paginator.get_page(page_number)
    
    milestone_types = Milestone.MILESTONE_TYPES
    
    context = {
        'milestones': milestones,
        'milestone_types': milestone_types,
        'current_type': type_filter,
    }
    return render(request, 'history/milestones.html', context)


@login_required
def contribute_history(request):
    if request.method == 'POST':
        contributor_name = request.POST.get('contributor_name')
        contributor_email = request.POST.get('contributor_email')
        title = request.POST.get('title')
        content = request.POST.get('content')
        supporting_documents = request.FILES.get('supporting_documents')
        images = request.FILES.get('images')
        
        if all([contributor_name, title, content]):
            HistoryContribution.objects.create(
                contributor_name=contributor_name,
                contributor_email=contributor_email,
                title=title,
                content=content,
                supporting_documents=supporting_documents,
                images=images,
                submitted_by=request.user
            )
            messages.success(request, 'Thank you for your contribution! It will be reviewed and added to our history.')
            return redirect('history:fellowship_history')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'history/contribute_history.html')


def events(request):
    events_list = HistoryEvent.objects.filter(is_approved=True)
    
    # Filter by category if specified
    category_filter = request.GET.get('category')
    if category_filter:
        events_list = events_list.filter(category_id=category_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        events_list = events_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    paginator = Paginator(events_list, 12)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    
    categories = HistoryCategory.objects.all()
    
    context = {
        'events': events,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'history/events.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(HistoryEvent, id=event_id, is_approved=True)
    
    # Get related events from the same category
    related_events = HistoryEvent.objects.filter(
        category=event.category,
        is_approved=True
    ).exclude(id=event.id)[:4]
    
    context = {
        'event': event,
        'related_events': related_events,
    }
    return render(request, 'history/event_detail.html', context)
