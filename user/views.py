from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, FormView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import (
    User
)
from .forms import (
    UserCreateForm
)

# Create your views here.


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'user/create_user.html'
    success_url = reverse_lazy("")


class UserListView(ListView):
    model = User
    template_name = 'user/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Shahin'
        return context
    

class UpdateUserView(UpdateView):
    model = User
    form_class = UserCreateForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy("user_list")


class UserDetailview(DetailView):
    model = User
    template_name = 'user/user_detail.html'



