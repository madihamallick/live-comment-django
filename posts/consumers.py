import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Comment, Post
from asgiref.sync import sync_to_async

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = f'post_{self.post_id}'

        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.post_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        author = data['author']
        content = data['content']

        post = await sync_to_async(Post.objects.get)(pk=self.post_id)
        comment = await sync_to_async(Comment.objects.create)(
            post=post, author=author, content=content
        )

        await self.channel_layer.group_send(
            self.post_group_name,
            {
                'type': 'new_comment',
                'author': author,
                'content': content,
            }
        )

    async def new_comment(self, event):
        await self.send(text_data=json.dumps({
            'author': event['author'],
            'content': event['content'],
        }))
