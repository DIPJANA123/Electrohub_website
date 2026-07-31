from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User

def signup_view(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            phone=request.POST['phone'],
            email=request.POST['email']
        )
        login(request, user)
        return redirect('homepage')
    return render(request, 'users/signup.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('homepage')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')
