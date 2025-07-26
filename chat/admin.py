from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'created_at', 'is_active']
    list_filter = ['room_type', 'is_active', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['participants']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender', 'content', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['content', 'sender__username', 'room__name']
    readonly_fields = ['timestamp']
