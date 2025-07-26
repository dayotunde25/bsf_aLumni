from django.contrib import admin
from .models import HistoryCategory, HistoryEvent, ExecutiveHistory, Milestone, HistoryContribution


@admin.register(HistoryCategory)
class HistoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'color', 'icon']
    search_fields = ['name', 'description']


@admin.register(HistoryEvent)
class HistoryEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'event_date', 'location', 'created_by', 'is_approved', 'is_featured']
    list_filter = ['category', 'is_approved', 'is_featured', 'event_date']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_approved', 'is_featured']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'event_date'


@admin.register(ExecutiveHistory)
class ExecutiveHistoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'session', 'start_year', 'end_year', 'is_approved']
    list_filter = ['position', 'is_approved', 'start_year']
    search_fields = ['name', 'session', 'bio', 'current_occupation']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'milestone_type', 'date', 'created_by', 'is_approved', 'is_featured']
    list_filter = ['milestone_type', 'is_approved', 'is_featured', 'date']
    search_fields = ['title', 'description']
    list_editable = ['is_approved', 'is_featured']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'


@admin.register(HistoryContribution)
class HistoryContributionAdmin(admin.ModelAdmin):
    list_display = ['title', 'contributor_name', 'submitted_by', 'submitted_at', 'is_reviewed']
    list_filter = ['is_reviewed', 'submitted_at']
    search_fields = ['title', 'contributor_name', 'content']
    list_editable = ['is_reviewed']
    readonly_fields = ['submitted_at']
