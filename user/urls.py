from django.urls import path
from .views import *

urlpatterns = [
    path('create_user/', UserCreateView.as_view(), name = 'create_user'),
    path('user_list/', UserListView.as_view(), name = 'user_list'),
    path('update_user/<pk>/', UpdateUserView.as_view(), name = 'update_user'),
    path('user_details/<pk>/', UserDetailview.as_view(), name = 'user_details'),
]
