from django.contrib.auth.models import AbstractUser
from django.db import models
import json

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('alumnus', 'Alumnus'),
        ('admin', 'Admin'),
    ]
    
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    birthday_month = models.IntegerField(null=True, blank=True)
    birthday_day = models.IntegerField(null=True, blank=True)
    fellowship_years = models.TextField(default='[]', help_text='JSON list of fellowship years')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    bio = models.TextField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_fellowship_years(self):
        """Get fellowship years as a Python list"""
        try:
            return json.loads(self.fellowship_years)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_fellowship_years(self, years_list):
        """Set fellowship years from a Python list"""
        self.fellowship_years = json.dumps(years_list)

class ExecutiveRole(models.Model):
    EXECUTIVE_CHOICES = [
        ('President(Pastor)', 'President(Pastor)'),
        ('Vice President(Bishop)', 'Vice President(Bishop)'),
        ('General Secretary', 'General Secretary'),
        ('Sisters Cordinator', 'Sisters Cordinator'),
        ('Brothers Cordinator', 'Brothers Cordinator'),
        ('Treasurer(CBN)', 'Treasurer(CBN)'),
        ('Choir Cordinator', 'Choir Cordinator'),
        ('Drama Cordinator', 'Drama Cordinator'),
        ('Bible Cordinator', 'Bible Cordinator'),
        ('Discipleship Cordinator', 'Discipleship Cordinator'),
        ('Prayer Cordinator', 'Prayer Cordinator'),
        ('Evangelism Cordinator', 'Evangelism Cordinator'),
        ('Publicity/Editorial Cordinator', 'Publicity/Editorial Cordinator'),
        ('Organizing Cordinator', 'Organizing Cordinator'),
        ('Librarian', 'Librarian'),
        ('Ushering Cordinator(Chief Usher)', 'Ushering Cordinator(Chief Usher)'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='executive_roles')
    position = models.CharField(max_length=100, choices=EXECUTIVE_CHOICES)
    session = models.CharField(max_length=20)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

class WorkerUnit(models.Model):
    UNIT_CHOICES = [
        ('Organizing', 'Organizing'),
        ('Prayer', 'Prayer'),
        ('Ushering', 'Ushering'),
        ('Bible', 'Bible'),
        ('Choir', 'Choir'),
        ('Evangelism/Visitation', 'Evangelism/Visitation'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_units')
    unit_name = models.CharField(max_length=100, choices=UNIT_CHOICES)
    session = models.CharField(max_length=20)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

class Post(models.Model):
    POST_CHOICES = [
        ('Family Head', 'Family Head'),
        ('Academic Chairman', 'Academic Chairman'),
        ('FYB Chairperson', 'FYB Chairperson'),
        ('House Cordinator', 'House Cordinator'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_name = models.CharField(max_length=100, choices=POST_CHOICES)
    session = models.CharField(max_length=20)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

class Level(models.Model):
    LEVEL_CHOICES = [
        ('ND1', 'ND1'),
        ('ND2', 'ND2'),
        ('HND1', 'HND1'),
        ('HND2', 'HND2'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='levels')
    level_name = models.CharField(max_length=100, choices=LEVEL_CHOICES)
    session = models.CharField(max_length=20)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
