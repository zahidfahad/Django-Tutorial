from django.urls import path
from .views import *


urlpatterns = [
    path('chat/<int:other_user_id>/', ChatView.as_view(), name = 'chat'),
    path('web-socket/chat/<int:other_user_id>/', WebSocketChatView.as_view(), name = 'socket_chat'),
]