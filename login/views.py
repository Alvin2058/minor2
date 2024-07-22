#login views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth import authenticate

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user using username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication successful, log in the user
            login(request, user)

            # Check if the logged-in user is an admin
            if user.is_superuser:
                # Redirect to admin-specific page or dashboard
                return redirect('admin:index')  # Replace with your admin URL name
            else:
                # Redirect to the home page or user-specific page
                return redirect('home')  # Replace with your desired URL name
        else:
            # If authentication fails, display error message
            messages.error(request, 'Invalid username or password.')

    # If request method is GET or authentication failed, render the login form
    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')



def register_view(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validation logic
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        else:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.first_name = fname
            user.last_name = lname
            user.save()

            messages.success(request, "Registration successful. Please log in.")

            return redirect('login')  

    return render(request, 'login/register.html')
