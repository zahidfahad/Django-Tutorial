from re import template
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
from chat.models import (
    DialogsModel,MessageModel
)

# Create your views here.

class ChatView(LoginRequiredMixin,View):
    template_name = 'chat/chat.html'

        
    def get_thread_name(self, logged_user_id, other_user_id):
        logged_user_id_is_bigger = logged_user_id > other_user_id
        if logged_user_id_is_bigger:
            thread_name = f'chat_{logged_user_id}-{other_user_id}'
        else:
            thread_name = thread_name = f'chat_{other_user_id}-{logged_user_id}'
        return thread_name
    
    
    def get(self, request, *args, **kwargs):
        logged_user = request.user
        other_user = User.objects.get(id=self.kwargs['other_user_id'])
        thread_name = self.get_thread_name(logged_user.id,other_user.id)
        
        context = {}
        context['other_user'] = other_user
        context["dialogs"] = DialogsModel.get_dialogs_for_user(self.request.user)
        context['conversation'] = MessageModel.objects.filter(thread_name=thread_name)
        context['conversation_length'] = len(context['conversation'])
        return render(request,self.template_name,context)
    
    
    def post(self, request, *args, **kwargs):
        MessageModel.objects.create(
            thread_name = self.get_thread_name(request.user.id,self.kwargs['other_user_id']),
            sender = request.user,
            receiver_id = self.kwargs['other_user_id'],
            text = request.POST['chat_input'],
        )
        return redirect('chat',self.kwargs['other_user_id'])