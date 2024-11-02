import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Comment, ReplyOnComment
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()
class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.premise_id = self.scope['url_route']['kwargs']['premise_id']
        self.room_group_name = f'premise_{self.premise_id}'

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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        # recive the rest we need for ai reply

        if 'parent_id' in text_data_json:
            parent_id = text_data_json['parent_id']
            await self.save_reply(user.id, message, parent_id)
        else:
            await self.save_comment(user.id, message)

        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user.username,
                    'is_reply': 'parent_id' in text_data_json,
                    'parent_id': parent_id if 'parent_id' in text_data_json else None
                }
            )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        is_reply = event.get('is_reply', False)
        parent_id = event.get('parent_id', None)

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'is_reply': is_reply,
            'parent_id': parent_id if parent_id else None
        }))

    @database_sync_to_async
    def save_comment(self, user_id, message):
        print(f"Saving comment for premise_id: {self.premise_id}")
        Comment.objects.create(user_id=user_id, premise_id=self.premise_id, text=message)
        # add ai reply according the all condn add the codes here
        # If suggest handle that as well

    @database_sync_to_async
    def save_reply(self, user_id, message, parent_id):
        if not User.objects.filter(id=user_id).exists():
            print("User does not exist:", user_id)
            return

        if not Comment.objects.filter(id=parent_id).exists():
            print("Parent comment does not exist:", parent_id)
            return

        ReplyOnComment.objects.create(user_id=user_id, text=message, reply_id=parent_id)
        # add ai reply according the all condn add the codes here