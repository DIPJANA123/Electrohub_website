from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User
from accounts.models import Customer

def signup_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'users/signup.html', {
                'error': 'Username already exists!'
            })

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'users/signup.html', {
                'error': 'Email already exists!'
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            phone=phone,
            email=email
        )

        Customer.objects.create(
            name=username,
            email=email,
            phone=phone,
            password=password
        )

        login(request, user)

        return redirect('homepage')

    return render(request, 'users/signup.html')

from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is not None:
             

               Customer.objects.get_or_create(
               email=user.email,
               defaults={
               'name': user.username,
               'phone': user.phone,
               'password': user.password
            }
               )

               login(request, user)
               return redirect('homepage')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('homepage')