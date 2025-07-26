from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from users.models import User
from events.models import Announcement
from gallery.models import MediaItem

@login_required
def home(request):
    # Get today's birthdays
    today = date.today()
    birthday_users = User.objects.filter(
        birthday_month=today.month,
        birthday_day=today.day
    )
    
    # Get recent announcements
    recent_announcements = Announcement.objects.filter(
        is_active=True
    ).order_by('-created_at')[:5]
    
    # Get recent gallery items
    recent_media = MediaItem.objects.filter(
        is_approved=True
    ).order_by('-uploaded_at')[:6]
    
    context = {
        'birthday_users': birthday_users,
        'recent_announcements': recent_announcements,
        'recent_media': recent_media,
    }
    return render(request, 'dashboard/home.html', context)