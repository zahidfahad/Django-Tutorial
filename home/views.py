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
from user.models import (
    User
)





class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context