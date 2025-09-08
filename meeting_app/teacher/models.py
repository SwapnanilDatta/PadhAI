from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    class Meta:
        app_label = 'teacher'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
