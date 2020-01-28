from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.messages import constants as messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')
 
    else:
        f = CustomUserCreationForm()
 
    return render(request, 'signup.html', {'form': f})





def logout(request):
    auth.logout(request)
    return render(request,'logout.html')

def login(request):
    if request.user.is_authenticated:
        return render(request, 'loggedin.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
 
        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return render(request, 'loggedin.html')
 
        else:
            messages.error(request, 'Error wrong username/password')
 
    return render(request, 'login.html')

