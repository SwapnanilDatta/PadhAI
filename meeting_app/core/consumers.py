import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom, Message, Meeting, WhiteboardData

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'chat_message':
            message = data['message']
            username = data['username']
            
            # Save message to database
            await self.save_message(message, username)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'timestamp': data.get('timestamp')
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def save_message(self, message, username):
        try:
            user = User.objects.get(username=username)
            room = ChatRoom.objects.get(id=self.room_id)
            Message.objects.create(room=room, sender=user, content=message)
        except Exception as e:
            print(f"Error saving message: {e}")
            # Don't raise the exception to prevent breaking the chat flow

class MeetingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'meeting_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'whiteboard_draw':
            # Broadcast whiteboard drawing data
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'whiteboard_update',
                    'data': data['data']
                }
            )
        elif message_type == 'webrtc_signal':
            # Handle WebRTC signaling
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_signal',
                    'signal': data['signal'],
                    'sender': data['sender']
                }
            )

    async def whiteboard_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'whiteboard_update',
            'data': event['data']
        }))

    async def webrtc_signal(self, event):
        await self.send(text_data=json.dumps({
            'type': 'webrtc_signal',
            'signal': event['signal'],
            'sender': event['sender']
        }))