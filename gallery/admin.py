from django.contrib import admin
from .models import Event, MediaItem


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'event', 'session', 'uploaded_by', 'uploaded_at', 'is_approved']
    list_filter = ['media_type', 'event', 'is_approved', 'uploaded_at']
    search_fields = ['title', 'description', 'uploaded_by__username']
    list_editable = ['is_approved']
    readonly_fields = ['uploaded_at']
