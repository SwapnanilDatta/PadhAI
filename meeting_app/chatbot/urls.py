from django.urls import path
from .views import register_view, login_view, logout_view, home_view, chat_detail_view, chat_list_view, new_chat_view, upload_file_view, download_notes

urlpatterns = [
    
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('chats/', chat_list_view, name='chat_list'),
    path('chats/new/', new_chat_view, name='new_chat'),
    path('chats/<int:session_id>/', chat_detail_view, name='chat_detail'),
    path('chats/<int:session_id>/download/', download_notes, name='download_notes'),
    path('upload/', upload_file_view, name='upload'),
    
]
