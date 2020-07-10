from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from polls.models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
        help_texts = {
            'username' : 'Required. 150 characters or fewer',
            'password1' : 'a',
            'password2' : 'Enter the same password as above , for verification'
        }
        
