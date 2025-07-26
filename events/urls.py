from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('announcements/', views.announcements, name='announcements'),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
]
