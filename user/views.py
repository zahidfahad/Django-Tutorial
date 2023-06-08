from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import HttpResponseRedirect, redirect
from django.views.generic.edit import FormView
from django.views.generic import View

from .forms import (
    LoginForm
)

# Create your views here.



class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = self.get_form()
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request,username=username,password=password)
        if user is None:
            messages.warning(self.request,"Wrong Credentials")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        
        login(self.request,user)
        return super().form_valid(form)
    

class Logout(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

