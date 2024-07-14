from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already login. Logout first")
            # return redirect("login")
        return render(request, "account/login.html")

    def post(self, request):
        uname = request.POST.get("username", "")
        passwd = request.POST.get("password", "")
        user = authenticate(username=uname, password=passwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in")
            # return redirect("index")
        else:
            messages.warning(request, "Username or password is incorrect")
        return render(request, "account/login.html")

@method_decorator(login_required, name="dispatch")
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("login")

class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in")
            # return redirect("index")  # Redirect to index or dashboard if logged in
        return render(request, "account/register.html")
    
    def post(self, request):
        uname = request.POST.get("username", "")
        email = request.POST.get("email", "")
        passwd = request.POST.get("password", "")
        
        # Check if user already exists
        if User.objects.filter(username=uname).exists():
            messages.info(request, "User already exists.")
            return redirect("register")  # Redirect to register page if user exists
        
        # Create new user if not already exists
        user = User.objects.create_user(username=uname, email=email,password=passwd)
        login(request, user)  # Automatically log in the user after registration
        messages.success(request, "User created and logged in")
        
        return redirect("login")  # Redirect to login page after successful registration