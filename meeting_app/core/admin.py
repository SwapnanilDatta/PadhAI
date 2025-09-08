
from django.contrib import admin
from .models import FriendRequest, Friendship, ChatRoom, Message, Meeting, WhiteboardData

admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(Meeting)
admin.site.register(WhiteboardData)