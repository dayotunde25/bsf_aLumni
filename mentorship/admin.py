from django.contrib import admin
from .models import MentorProfile, MentorshipRequest, Mentorship, MentorshipSession, MentorshipFeedback


@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'years_of_experience', 'max_mentees', 'current_mentees_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'years_of_experience', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at', 'current_mentees_count']


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ['mentee', 'mentor', 'area_of_interest', 'status', 'created_at']
    list_filter = ['status', 'area_of_interest', 'created_at']
    search_fields = ['mentee__username', 'mentor__user__username', 'message']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'mentee', 'area_of_focus', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'area_of_focus', 'start_date']
    search_fields = ['mentor__user__username', 'mentee__username', 'goals']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display = ['mentorship', 'session_type', 'scheduled_date', 'duration_minutes', 'is_completed']
    list_filter = ['session_type', 'is_completed', 'scheduled_date']
    search_fields = ['mentorship__mentor__user__username', 'mentorship__mentee__username', 'notes']
    list_editable = ['is_completed']
    readonly_fields = ['created_at']


@admin.register(MentorshipFeedback)
class MentorshipFeedbackAdmin(admin.ModelAdmin):
    list_display = ['mentorship', 'given_by', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['mentorship__mentor__user__username', 'mentorship__mentee__username', 'given_by__username', 'comment']
    readonly_fields = ['created_at']
