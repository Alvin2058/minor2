from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserUpdateForm
from quiz.models import Mark 

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user using username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect to the next page if 'next' parameter is in the request
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            if user.is_superuser:
                # Redirect to admin-specific page or dashboard
                return redirect(reverse('admin:index'))  # Replace with your admin URL name
            else:
                # Redirect to the home page or user-specific page
                return redirect(reverse('home'))  # Replace with your desired URL name
        else:
            # If authentication fails, display error message
            messages.error(request, 'Invalid username or password.')

    # If request method is GET or authentication failed, render the login form
    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect(reverse('home'))

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

            return redirect(reverse('login'))  # Replace with your login URL name

    return render(request, 'login/register.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(instance=request.user, data=request.POST)
        profile_form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'login/profile.html', context)

@login_required
def quiz_history_view(request):
    history = Mark.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'login/history_table.html', {
        'history': history
    })