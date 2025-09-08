from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from .models import FriendRequest, Friendship, ChatRoom, Message, Meeting
from teacher.models import Teacher
import json

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    is_teacher = Teacher.objects.filter(user=request.user).exists()
    friends = get_user_friends(request.user)
    pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    context = {
        'friends': friends,
        'pending_requests': pending_requests,
        'is_teacher': is_teacher
    }
    if not is_teacher:
        teachers = Teacher.objects.select_related('user').all()
        context['teachers'] = teachers
    return render(request, 'meetings/dashboard.html', context)

@login_required
def send_friend_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            to_user = User.objects.get(username=username)
            if to_user != request.user:
                friend_request, created = FriendRequest.objects.get_or_create(
                    from_user=request.user,
                    to_user=to_user,
                    defaults={'status': 'pending'}
                )
                if created:
                    return JsonResponse({'success': True, 'message': 'Friend request sent!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Request already exists'})
            else:
                return JsonResponse({'success': False, 'message': "You can't send request to yourself"})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def handle_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            
            # Create friendship
            Friendship.objects.create(
                user1=friend_request.from_user,
                user2=friend_request.to_user
            )
            
            # Create chat room for the friends
            chat_room = ChatRoom.objects.create()
            chat_room.participants.add(friend_request.from_user, friend_request.to_user)
            
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
    
    return redirect('dashboard')

@login_required
def chat_room(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    
    # Check if user is participant
    if request.user not in chat_room.participants.all():
        return redirect('dashboard')
    
    messages = chat_room.messages.all().order_by('timestamp')
    other_participant = chat_room.participants.exclude(id=request.user.id).first()
    
    return render(request, 'meetings/chat_room.html', {
        'room': chat_room,
        'messages': messages,
        'other_participant': other_participant
    })

@login_required
def start_meeting(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    
    if request.user not in chat_room.participants.all():
        return redirect('dashboard')
    
    meeting, created = Meeting.objects.get_or_create(
        room=chat_room,
        status='waiting',
        defaults={'created_by': request.user}
    )
    
    return render(request, 'meetings/meeting_room.html', {
        'meeting': meeting,
        'room': chat_room
    })

def get_user_friends(user):
    friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
    friends = []
    for friendship in friendships:
        friend = friendship.user2 if friendship.user1 == user else friendship.user1
        # Get or create chat room for these friends
        chat_room = ChatRoom.objects.filter(participants=user).filter(participants=friend).first()
        friends.append({'user': friend, 'chat_room': chat_room})
    return friends
