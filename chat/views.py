from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import ChatRoom, Message
from users.models import User


@login_required
def chat_rooms(request):
    # Get user's chat rooms
    user_rooms = request.user.chat_rooms.filter(is_active=True)
    
    context = {'chat_rooms': user_rooms}
    return render(request, 'chat/chat_rooms.html', context)


@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
    
    # Check if user is a participant
    if not room.participants.filter(id=request.user.id).exists():
        messages.error(request, 'You are not authorized to access this chat room.')
        return redirect('chat:chat_rooms')
    
    # Get messages
    messages_list = room.messages.all().order_by('timestamp')
    
    # Mark messages as read
    unread_messages = messages_list.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True)
    
    context = {
        'room': room,
        'messages': messages_list,
    }
    return render(request, 'chat/chat_room.html', context)


@login_required
def start_private_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user.role == 'admin':
        messages.error(request, 'You cannot start a chat with an administrator.')
        return redirect('users:directory')

    if other_user == request.user:
        messages.error(request, 'You cannot start a chat with yourself.')
        return redirect('users:directory')
    
    # Check if private chat already exists
    existing_room = ChatRoom.objects.filter(
        room_type='private',
        participants=request.user
    ).filter(participants=other_user).first()
    
    if existing_room:
        return redirect('chat:chat_room', room_id=existing_room.id)
    
    # Create new private chat room
    room = ChatRoom.objects.create(
        name=f"Chat between {request.user.username} and {other_user.username}",
        room_type='private'
    )
    room.participants.add(request.user, other_user)
    
    return redirect('chat:chat_room', room_id=room.id)


@login_required
def send_message(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        
        # Check if user is a participant
        if not room.participants.filter(id=request.user.id).exists():
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'})
        
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                room=room,
                sender=request.user,
                content=content
            )
            
            return JsonResponse({
                'status': 'success',
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'sender': message.sender.username,
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def get_messages(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
    
    # Check if user is a participant
    if not room.participants.filter(id=request.user.id).exists():
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'})
    
    messages_list = room.messages.all().order_by('timestamp')
    messages_data = []
    
    for message in messages_list:
        messages_data.append({
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'sender_id': message.sender.id,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': message.is_read
        })
    
    return JsonResponse({'status': 'success', 'messages': messages_data})
