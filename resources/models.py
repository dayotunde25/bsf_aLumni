from django.db import models
from users.models import User
import json


class ResourceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    class Meta:
        verbose_name_plural = 'Resource Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Resource(models.Model):
    RESOURCE_TYPES = [
        ('pdf', 'PDF Document'),
        ('audio', 'Audio File'),
        ('video', 'Video File'),
        ('link', 'External Link'),
        ('image', 'Image'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='resources')
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    external_url = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_resources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    download_count = models.PositiveIntegerField(default=0)
    tags = models.TextField(default='[]', blank=True, help_text='JSON list of tags')
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.title
    
    def increment_downloads(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])
    
    @property
    def file_size_mb(self):
        if self.file:
            return round(self.file.size / (1024 * 1024), 2)
        return 0

    def get_tags(self):
        """Get tags as a Python list"""
        try:
            return json.loads(self.tags)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_tags(self, tags_list):
        """Set tags from a Python list"""
        self.tags = json.dumps(tags_list)


class ResourceDownload(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_downloads')
    downloaded_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.user.username} downloaded {self.resource.title}"


class ResourceRating(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['resource', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} rated {self.resource.title} - {self.rating}/5"


class ResourceBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_resources')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'resource']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.resource.title}"
