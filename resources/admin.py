from django.contrib import admin
from .models import ResourceCategory, Resource, ResourceDownload, ResourceRating, ResourceBookmark


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon']
    search_fields = ['name', 'description']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'category', 'author', 'uploaded_by', 'created_at', 'is_approved', 'is_featured', 'download_count']
    list_filter = ['resource_type', 'category', 'is_approved', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'author', 'uploaded_by__username']
    list_editable = ['is_approved', 'is_featured']
    readonly_fields = ['created_at', 'updated_at', 'download_count', 'file_size_mb']
    filter_horizontal = []


@admin.register(ResourceDownload)
class ResourceDownloadAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'downloaded_at', 'ip_address']
    list_filter = ['downloaded_at']
    search_fields = ['resource__title', 'user__username']
    readonly_fields = ['downloaded_at']


@admin.register(ResourceRating)
class ResourceRatingAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['resource__title', 'user__username', 'comment']
    readonly_fields = ['created_at']


@admin.register(ResourceBookmark)
class ResourceBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'resource__title']
    readonly_fields = ['created_at']
