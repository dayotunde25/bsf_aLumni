from django.db import models
from users.models import User


class Announcement(models.Model):
    ANNOUNCEMENT_TYPES = [
        ('general', 'General'),
        ('event', 'Event'),
        ('urgent', 'Urgent'),
        ('fellowship', 'Fellowship'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    announcement_type = models.CharField(max_length=20, choices=ANNOUNCEMENT_TYPES, default='general')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    requires_rsvp = models.BooleanField(default=False)
    max_attendees = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['event_date']
    
    def __str__(self):
        return self.title
    
    @property
    def attendee_count(self):
        return self.rsvps.filter(status='attending').count()


class RSVP(models.Model):
    STATUS_CHOICES = [
        ('attending', 'Attending'),
        ('not_attending', 'Not Attending'),
        ('maybe', 'Maybe'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['event', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"
