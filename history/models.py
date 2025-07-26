from django.db import models
from users.models import User


class HistoryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#28a745', help_text="Hex color code")
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    class Meta:
        verbose_name_plural = 'History Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class HistoryEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(HistoryCategory, on_delete=models.CASCADE, related_name='events')
    event_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="For events spanning multiple days")
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='history/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['event_date']
    
    def __str__(self):
        return f"{self.title} ({self.event_date.year})"
    
    @property
    def year(self):
        return self.event_date.year


class ExecutiveHistory(models.Model):
    POSITION_CHOICES = [
        ('president', 'President'),
        ('vice_president', 'Vice President'),
        ('secretary', 'Secretary'),
        ('treasurer', 'Treasurer'),
        ('financial_secretary', 'Financial Secretary'),
        ('publicity_secretary', 'Publicity Secretary'),
        ('social_secretary', 'Social Secretary'),
        ('welfare_secretary', 'Welfare Secretary'),
        ('chaplain', 'Chaplain'),
        ('provost', 'Provost'),
        ('assistant_secretary', 'Assistant Secretary'),
        ('ex_officio', 'Ex-Officio'),
    ]
    
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    session = models.CharField(max_length=20, help_text="e.g., 2020/2021")
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    photo = models.ImageField(upload_to='executives/', blank=True, null=True)
    bio = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    current_occupation = models.CharField(max_length=200, blank=True)
    contact_info = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='executive_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_year', 'position']
        verbose_name_plural = 'Executive Histories'
    
    def __str__(self):
        return f"{self.name} - {self.get_position_display()} ({self.session})"


class Milestone(models.Model):
    MILESTONE_TYPES = [
        ('founding', 'Founding'),
        ('anniversary', 'Anniversary'),
        ('revival', 'Revival/Outreach'),
        ('achievement', 'Achievement'),
        ('expansion', 'Expansion'),
        ('partnership', 'Partnership'),
        ('award', 'Award/Recognition'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    milestone_type = models.CharField(max_length=20, choices=MILESTONE_TYPES)
    date = models.DateField()
    image = models.ImageField(upload_to='milestones/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='milestones')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return f"{self.title} ({self.date.year})"


class HistoryContribution(models.Model):
    contributor_name = models.CharField(max_length=200)
    contributor_email = models.EmailField(blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    supporting_documents = models.FileField(upload_to='history_contributions/', blank=True, null=True)
    images = models.ImageField(upload_to='history_contributions/', blank=True, null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history_contributions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    reviewer_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"Contribution: {self.title} by {self.contributor_name}"
