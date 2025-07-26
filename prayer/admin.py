from django.contrib import admin
from .models import PrayerRequest, Prayer, PrayerComment, Testimony, TestimonyLike


@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'requested_by', 'created_at', 'is_answered', 'is_approved', 'prayer_count']
    list_filter = ['category', 'is_answered', 'is_approved', 'is_anonymous', 'created_at']
    search_fields = ['title', 'description', 'requested_by__username']
    list_editable = ['is_answered', 'is_approved']
    readonly_fields = ['created_at', 'updated_at', 'prayer_count']


@admin.register(Prayer)
class PrayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'prayer_request', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'prayer_request__title']


@admin.register(PrayerComment)
class PrayerCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'prayer_request', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'prayer_request__title', 'content']


@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_approved', 'is_anonymous']
    list_filter = ['is_approved', 'is_anonymous', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['is_approved']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TestimonyLike)
class TestimonyLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'testimony', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'testimony__title']
