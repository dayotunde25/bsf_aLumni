from django.db import models
from users.models import User


class PrayerRequest(models.Model):
    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('family', 'Family'),
        ('health', 'Health'),
        ('financial', 'Financial'),
        ('spiritual', 'Spiritual'),
        ('fellowship', 'Fellowship'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prayer_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_answered = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def prayer_count(self):
        return self.prayers.count()


class Prayer(models.Model):
    prayer_request = models.ForeignKey(PrayerRequest, on_delete=models.CASCADE, related_name='prayers')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['prayer_request', 'user']
    
    def __str__(self):
        return f"{self.user.username} praying for {self.prayer_request.title}"


class PrayerComment(models.Model):
    prayer_request = models.ForeignKey(PrayerRequest, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.prayer_request.title}"


class Testimony(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Testimonies'
    
    def __str__(self):
        return self.title


class TestimonyLike(models.Model):
    testimony = models.ForeignKey(Testimony, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['testimony', 'user']
    
    def __str__(self):
        return f"{self.user.username} likes {self.testimony.title}"
