from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', Logout.as_view(), name= 'logout'),
    path('search/', Search.as_view(), name= 'search'),
]
