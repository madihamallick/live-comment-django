from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/comments/<int:post_id>/', consumers.CommentConsumer.as_asgi()),
]