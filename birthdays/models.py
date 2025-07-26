from django.db import models
from users.models import User

class BirthdayNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_sent = models.DateField(auto_now_add=True)
    notification_type = models.CharField(max_length=20, default='birthday')