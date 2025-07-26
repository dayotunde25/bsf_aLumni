from django.contrib import admin
from .models import Announcement, Event, RSVP


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'announcement_type', 'created_by', 'created_at', 'is_active', 'is_pinned']
    list_filter = ['announcement_type', 'is_active', 'is_pinned', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['is_active', 'is_pinned']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'location', 'created_by', 'requires_rsvp', 'attendee_count', 'is_active']
    list_filter = ['requires_rsvp', 'is_active', 'event_date']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'attendee_count']


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'event__title']
