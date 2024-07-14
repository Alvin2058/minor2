#login views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import authenticate


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page (e.g., home)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_pw = request.POST.get('confirm_pw')
        
        if password != confirm_pw:
            messages.error(request, "Passwords do not match.")
        else:
            # Create the user
            user = User.objects.create_user(email=email, password=password)
            user.name = name  # You might need to adjust this depending on your User model
            user.save()
            # Log in the user after registration
            login(request, user)
            # Redirect to a success page (e.g., home)
            return redirect('home')
            
    return render(request, 'register.html')

