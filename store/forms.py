from django import forms
from django.contrib.auth.forms import UserCreationForm
from store.models import User


class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']
        

class LoginForm(forms.Form):
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())