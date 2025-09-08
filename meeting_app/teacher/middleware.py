from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.contrib import messages
from .models import Teacher

class TeacherMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view is called
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip middleware for non-authenticated users
        if not request.user.is_authenticated:
            return None

        # Get current URL path
        path = request.path_info
        url_name = resolve(path).url_name

        # Skip middleware for certain paths
        if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/media/'):
            return None

        # Check if user is accessing teacher-specific URLs
        if path.startswith('/teacher/'):
            try:
                # Check if user is a teacher
                teacher = Teacher.objects.get(user=request.user)
                # User is a teacher, allow access
                return None
            except Teacher.DoesNotExist:
                # User is not a teacher, redirect to home
                messages.error(request, 'You are not registered as a teacher')
                return redirect('core:home')

        return None