from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from .models import Teacher
from .decorators import teacher_required
from .forms import TeacherRegistrationForm, TeacherProfileForm

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher account created successfully. Please login.')
            return redirect('teacher:login')
    else:
        form = TeacherRegistrationForm()
    
    return render(request, 'teacher/register.html', {'form': form})

def login_teacher(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            try:
                teacher = Teacher.objects.get(user=user)
                login(request, user)
                return redirect('teacher:dashboard')
            except Teacher.DoesNotExist:
                messages.error(request, 'You are not registered as a teacher.')
                # Create a new form to clear the password field
                form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    
    return render(request, 'teacher/login.html', {'form': form})

@login_required
def logout_teacher(request):
    logout(request)
    return redirect('teacher:login')

@login_required
@teacher_required
def teacher_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('teacher:dashboard')
    else:
        form = TeacherProfileForm(instance=teacher)
    
    return render(request, 'teacher/dashboard.html', {'teacher': teacher, 'form': form})

@login_required
@teacher_required
def teacher_chatbot(request):
    return redirect('home')

@login_required
@teacher_required
def teacher_meetings(request):
    return redirect('dashboard')

@login_required
@teacher_required
def teacher_profile(request):
    teacher = Teacher.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('teacher:profile')
    else:
        form = TeacherProfileForm(instance=teacher)
    
    return render(request, 'teacher/profile.html', {'teacher': teacher, 'form': form})

@login_required
@teacher_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('teacher:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'teacher/change_password.html', {'form': form})
