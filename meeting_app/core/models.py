from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FriendRequest(models.Model):
    class Meta:
        app_label = 'core'
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

class Friendship(models.Model):
    class Meta:
        app_label = 'core'
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

class ChatRoom(models.Model):
    class Meta:
        app_label = 'core'
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def room_name(self):
        return f"chat_{self.id}"

class Message(models.Model):
    class Meta:
        app_label = 'core'
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Meeting(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('active', 'Active'),
        ('ended', 'Ended'),
    ]
    
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

class WhiteboardData(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='whiteboard_data')
    data = models.JSONField()  # Store drawing data as JSON
    created_at = models.DateTimeField(auto_now_add=True)