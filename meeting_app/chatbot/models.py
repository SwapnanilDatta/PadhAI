from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    class Meta:
        app_label = 'chatbot'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class ChatMessage(models.Model):
    class Meta:
        app_label = 'chatbot'
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('assistant', 'Assistant')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:30]}"

class UploadedFile(models.Model):
    class Meta:
        app_label = 'chatbot'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file} ({self.user.username})"