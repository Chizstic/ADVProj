from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Signup Form
class SignUpForm(UserCreationForm):
   
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)
