from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('register/', views.register_teacher, name='register'),
    path('login/', views.login_teacher, name='login'),
    path('logout/', views.logout_teacher, name='logout'),
    path('dashboard/', views.teacher_dashboard, name='dashboard'),
    path('profile/', views.teacher_profile, name='profile'),
    path('password/', views.change_password, name='change_password'),
    path('chatbot/', views.teacher_chatbot, name='chatbot'),
    path('meetings/', views.teacher_meetings, name='meetings'),
]