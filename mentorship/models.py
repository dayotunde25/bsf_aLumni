from django.db import models
from users.models import User
import json


class MentorProfile(models.Model):
    EXPERTISE_AREAS = [
        ('academic', 'Academic'),
        ('career', 'Career Development'),
        ('spiritual', 'Spiritual Growth'),
        ('leadership', 'Leadership'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('health', 'Health & Wellness'),
        ('relationships', 'Relationships'),
        ('ministry', 'Ministry'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField()
    expertise_areas = models.TextField(default='[]', help_text='JSON list of expertise areas')
    years_of_experience = models.PositiveIntegerField()
    availability = models.TextField(help_text="Describe your availability for mentoring")
    max_mentees = models.PositiveIntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Mentor: {self.user.get_full_name() or self.user.username}"

    def get_expertise_areas(self):
        """Get expertise areas as a Python list"""
        try:
            return json.loads(self.expertise_areas)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_expertise_areas(self, areas_list):
        """Set expertise areas from a Python list"""
        self.expertise_areas = json.dumps(areas_list)
    
    @property
    def current_mentees_count(self):
        return self.mentorships.filter(status='active').count()
    
    @property
    def can_accept_mentees(self):
        return self.is_active and self.current_mentees_count < self.max_mentees


class MentorshipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('cancelled', 'Cancelled'),
    ]
    
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_requests')
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='requests')
    message = models.TextField(help_text="Why do you want this mentor?")
    area_of_interest = models.CharField(max_length=50, choices=MentorProfile.EXPERTISE_AREAS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    response_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.mentee.username} -> {self.mentor.user.username} ({self.status})"


class Mentorship(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('terminated', 'Terminated'),
    ]
    
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='mentorships')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorships')
    area_of_focus = models.CharField(max_length=50, choices=MentorProfile.EXPERTISE_AREAS)
    goals = models.TextField(help_text="Mentorship goals and objectives")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['mentor', 'mentee']
    
    def __str__(self):
        return f"{self.mentor.user.username} mentoring {self.mentee.username}"


class MentorshipSession(models.Model):
    SESSION_TYPES = [
        ('video_call', 'Video Call'),
        ('phone_call', 'Phone Call'),
        ('in_person', 'In Person'),
        ('email', 'Email'),
        ('chat', 'Chat'),
    ]
    
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE, related_name='sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    scheduled_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"Session: {self.mentorship} on {self.scheduled_date.date()}"


class MentorshipFeedback(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE, related_name='feedback')
    given_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['mentorship', 'given_by']
    
    def __str__(self):
        return f"Feedback by {self.given_by.username} for {self.mentorship}"
