from django.urls import path
from posts.consumers import ChatConsumer

websocket_urlpatterns = [
    path("" , ChatConsumer.as_asgi()) ,
]