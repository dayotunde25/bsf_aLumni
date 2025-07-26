from django.contrib import admin
from .models import JobCategory, JobPosting, JobApplication, SavedJob


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'posted_by', 'created_at', 'is_approved', 'is_active', 'views_count']
    list_filter = ['job_type', 'experience_level', 'category', 'is_approved', 'is_active', 'created_at']
    search_fields = ['title', 'company', 'location', 'description']
    list_editable = ['is_approved', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'views_count']
    filter_horizontal = []


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['applicant__username', 'job__title', 'job__company']
    list_editable = ['status']
    readonly_fields = ['applied_at', 'updated_at']


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__username', 'job__title', 'job__company']
