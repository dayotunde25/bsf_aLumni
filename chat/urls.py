from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_rooms, name='chat_rooms'),
    path('room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('start/<int:user_id>/', views.start_private_chat, name='start_private_chat'),
    path('send/<int:room_id>/', views.send_message, name='send_message'),
    path('messages/<int:room_id>/', views.get_messages, name='get_messages'),
]
