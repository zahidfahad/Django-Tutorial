from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User
)


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','type': 'text'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control','type': 'password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control','type': 'password'})
        }
        
        
class LoginForm(forms.Form):
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    password = forms.CharField(widget= forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
