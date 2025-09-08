from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .models import Teacher

def teacher_required(view_func):
    """Decorator to check if the user is a teacher"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page')
            return redirect('teacher:login')
        
        try:
            teacher = Teacher.objects.get(user=request.user)
            return view_func(request, *args, **kwargs)
        except Teacher.DoesNotExist:
            messages.error(request, 'You are not registered as a teacher')
            return redirect('core:home')
    
    return _wrapped_view