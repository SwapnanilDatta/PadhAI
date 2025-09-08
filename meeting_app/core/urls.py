from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('send-friend-request/', views.send_friend_request, name='send_friend_request'),
    path('handle-request/<int:request_id>/', views.handle_friend_request, name='handle_friend_request'),
    path('chat/<int:room_id>/', views.chat_room, name='chat_room'),
    path('meeting/<int:room_id>/', views.start_meeting, name='start_meeting'),
]
