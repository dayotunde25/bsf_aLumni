from django.db import models
from users.models import User

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class MediaItem(models.Model):
    MEDIA_TYPES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='gallery/')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    session = models.CharField(max_length=20)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)