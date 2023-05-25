from django.urls import path
from .views import *


urlpatterns = [
    path('chat/<int:other_user_id>/', ChatView.as_view(), name = 'chat'),
]