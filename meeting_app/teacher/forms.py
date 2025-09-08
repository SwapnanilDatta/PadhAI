from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Teacher

class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            Teacher.objects.create(
                user=user,
                subject=self.cleaned_data['subject'],
                bio=self.cleaned_data['bio']
            )
        
        return user

class TeacherProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Teacher
        fields = ['subject', 'bio']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        teacher = super().save(commit=False)
        
        if commit:
            # Update User model fields
            user = teacher.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.save()
            
            # Save Teacher model
            teacher.save()
        
        return teacher