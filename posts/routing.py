from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/premise/<uuid:premise_id>/', consumers.CommentConsumer.as_asgi()),
]