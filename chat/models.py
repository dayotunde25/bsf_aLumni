from django.db import models
from users.models import User

class ChatRoom(models.Model):
    ROOM_TYPES = [
        ('private', 'Private'),
        ('group', 'Group'),
        ('broadcast', 'Broadcast'),
    ]
    
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)