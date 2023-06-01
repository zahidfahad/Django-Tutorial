# chat/routing.py
from django.urls import path

from .consumers import chat

websocket_urlpatterns = [
    path("ws/chat/<int:other_user_id>/", chat.ChatConsumer.as_asgi()),
]