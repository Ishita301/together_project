import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return
        partner = await self.get_partner()
        if not partner:
            await self.close()
            return
        ids = sorted([self.user.id, partner.id])
        self.room_name = f"chat_{ids[0]}_{ids[1]}"
        self.room_group_name = f"chat_{ids[0]}_{ids[1]}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type', 'message')
        if msg_type == 'typing':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'typing_indicator',
                'username': self.user.username,
                'is_typing': data.get('is_typing', False),
            })
        elif msg_type == 'message':
            content = data.get('message', '')
            partner = await self.get_partner()
            if content and partner:
                message = await self.save_message(content, partner)
                await self.channel_layer.group_send(self.room_group_name, {
                    'type': 'chat_message',
                    'message': content,
                    'sender_id': self.user.id,
                    'sender_name': self.user.username,
                    'sender_avatar': self.user.get_avatar_url(),
                    'timestamp': message.created_at.strftime('%I:%M %p'),
                    'message_id': message.id,
                })
        elif msg_type == 'seen':
            await self.mark_messages_seen()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'sender_avatar': event['sender_avatar'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id'],
        }))

    async def typing_indicator(self, event):
        if event['username'] != self.user.username:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'username': event['username'],
                'is_typing': event['is_typing'],
            }))

    @database_sync_to_async
    def get_partner(self):
        from accounts.models import User
        try:
            user = User.objects.get(id=self.user.id)
            return user.partner
        except:
            return None

    @database_sync_to_async
    def save_message(self, content, partner):
        from chat.models import Message
        return Message.objects.create(
            sender=self.user, receiver=partner, content=content
        )

    @database_sync_to_async
    def mark_messages_seen(self):
        from chat.models import Message
        Message.objects.filter(receiver=self.user, is_seen=False).update(
            is_seen=True, seen_at=timezone.now()
        )
