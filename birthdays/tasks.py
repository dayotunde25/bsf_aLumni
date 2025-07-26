from celery import shared_task
from datetime import date
from users.models import User
from .models import BirthdayNotification

@shared_task
def check_birthdays():
    today = date.today()
    birthday_users = User.objects.filter(
        birthday_month=today.month,
        birthday_day=today.day
    )
    
    for user in birthday_users:
        # Create notification if not already sent today
        if not BirthdayNotification.objects.filter(
            user=user, 
            date_sent=today
        ).exists():
            BirthdayNotification.objects.create(user=user)
    
    return f"Found {birthday_users.count()} birthdays today"