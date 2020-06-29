from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def register(response): 
    form = UserCreationForm()
    return render(response, 'register/register.html', {"form":form})