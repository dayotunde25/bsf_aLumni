from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from events.models import Announcement, Event
from gallery.models import Event as GalleryEvent
from prayer.models import PrayerRequest, Testimony
from jobs.models import JobCategory, JobPosting
from resources.models import ResourceCategory, Resource
from history.models import HistoryCategory, HistoryEvent, ExecutiveHistory, Milestone
from mentorship.models import MentorProfile
from datetime import date, datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for Baptist Student Fellowship'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        self.create_sample_users()
        
        # Create sample events and announcements
        self.create_sample_events()
        
        # Create sample gallery events
        self.create_sample_gallery_events()
        
        # Create sample prayer requests and testimonies
        self.create_sample_prayer_data()
        
        # Create sample job data
        self.create_sample_job_data()
        
        # Create sample resources
        self.create_sample_resources()
        
        # Create sample history data
        self.create_sample_history_data()
        
        # Create sample mentor profiles
        self.create_sample_mentors()
        
        self.stdout.write(self.style.SUCCESS('Successfully created sample data!'))

    def create_sample_users(self):
        sample_users = [
            {'username': 'john_doe', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', 'role': 'alumnus'},
            {'username': 'jane_smith', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com', 'role': 'alumnus'},
            {'username': 'mike_johnson', 'first_name': 'Mike', 'last_name': 'Johnson', 'email': 'mike@example.com', 'role': 'student'},
            {'username': 'sarah_wilson', 'first_name': 'Sarah', 'last_name': 'Wilson', 'email': 'sarah@example.com', 'role': 'student'},
            {'username': 'david_brown', 'first_name': 'David', 'last_name': 'Brown', 'email': 'david@example.com', 'role': 'alumnus'},
        ]
        
        for user_data in sample_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    password='password123',
                    birthday_month=random.randint(1, 12),
                    birthday_day=random.randint(1, 28),
                    **user_data
                )
                self.stdout.write(f'Created user: {user.username}')

    def create_sample_events(self):
        admin_user = User.objects.filter(role='admin').first()
        if not admin_user:
            admin_user = User.objects.first()
        
        announcements = [
            {'title': 'Welcome to New Session', 'content': 'We welcome all new and returning members to the new academic session.', 'announcement_type': 'general'},
            {'title': 'Prayer Meeting This Friday', 'content': 'Join us for our weekly prayer meeting this Friday at 6 PM.', 'announcement_type': 'fellowship'},
            {'title': 'Alumni Reunion 2024', 'content': 'Save the date for our annual alumni reunion coming up next month.', 'announcement_type': 'event'},
        ]
        
        for ann_data in announcements:
            if not Announcement.objects.filter(title=ann_data['title']).exists():
                Announcement.objects.create(
                    created_by=admin_user,
                    is_approved=True,
                    is_active=True,
                    **ann_data
                )
                self.stdout.write(f'Created announcement: {ann_data["title"]}')

    def create_sample_gallery_events(self):
        events = [
            {'name': 'Bible Study', 'description': 'Weekly Bible study sessions'},
            {'name': 'Cultural Day', 'description': 'Annual cultural celebration'},
            {'name': 'Outreach Program', 'description': 'Community outreach activities'},
            {'name': 'Fellowship Retreat', 'description': 'Annual fellowship retreat'},
        ]
        
        for event_data in events:
            if not GalleryEvent.objects.filter(name=event_data['name']).exists():
                GalleryEvent.objects.create(**event_data)
                self.stdout.write(f'Created gallery event: {event_data["name"]}')

    def create_sample_prayer_data(self):
        users = User.objects.all()[:3]
        
        prayer_requests = [
            {'title': 'Pray for Exam Success', 'description': 'Please pray for all students taking exams this semester.', 'category': 'spiritual'},
            {'title': 'Health and Healing', 'description': 'Pray for those who are sick in our fellowship.', 'category': 'health'},
            {'title': 'Financial Breakthrough', 'description': 'Pray for members facing financial challenges.', 'category': 'financial'},
        ]
        
        for i, prayer_data in enumerate(prayer_requests):
            if not PrayerRequest.objects.filter(title=prayer_data['title']).exists():
                PrayerRequest.objects.create(
                    requested_by=users[i % len(users)],
                    is_approved=True,
                    **prayer_data
                )
                self.stdout.write(f'Created prayer request: {prayer_data["title"]}')

    def create_sample_job_data(self):
        # Create job categories
        categories = [
            {'name': 'Technology', 'description': 'IT and Software Development jobs'},
            {'name': 'Education', 'description': 'Teaching and Educational roles'},
            {'name': 'Healthcare', 'description': 'Medical and Healthcare positions'},
            {'name': 'Business', 'description': 'Business and Management roles'},
        ]
        
        for cat_data in categories:
            category, created = JobCategory.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
            if created:
                self.stdout.write(f'Created job category: {cat_data["name"]}')

    def create_sample_resources(self):
        # Create resource categories
        categories = [
            {'name': 'Sermons', 'description': 'Audio and video sermons', 'icon': 'fas fa-microphone'},
            {'name': 'Devotionals', 'description': 'Daily devotional materials', 'icon': 'fas fa-book-open'},
            {'name': 'Study Materials', 'description': 'Bible study resources', 'icon': 'fas fa-graduation-cap'},
        ]
        
        for cat_data in categories:
            category, created = ResourceCategory.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
            if created:
                self.stdout.write(f'Created resource category: {cat_data["name"]}')

    def create_sample_history_data(self):
        # Create history categories
        categories = [
            {'name': 'Founding', 'description': 'Fellowship founding events', 'color': '#28a745'},
            {'name': 'Outreach', 'description': 'Evangelism and outreach programs', 'color': '#17a2b8'},
            {'name': 'Leadership', 'description': 'Leadership and executive events', 'color': '#ffc107'},
        ]
        
        for cat_data in categories:
            category, created = HistoryCategory.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
            if created:
                self.stdout.write(f'Created history category: {cat_data["name"]}')

    def create_sample_mentors(self):
        alumni_users = User.objects.filter(role='alumnus')[:2]
        
        for user in alumni_users:
            if not hasattr(user, 'mentor_profile'):
                mentor_profile = MentorProfile.objects.create(
                    user=user,
                    bio=f'Experienced professional willing to mentor students in various areas.',
                    years_of_experience=random.randint(3, 10),
                    availability='Weekends and evenings',
                    max_mentees=3,
                    is_active=True
                )
                mentor_profile.set_expertise_areas(['career', 'spiritual', 'leadership'])
                self.stdout.write(f'Created mentor profile for: {user.username}')
