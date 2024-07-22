# example/main-urls.py

from django.contrib import admin
from django.urls import path, include
from . import views  # Import views from the current directory

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name='home'),  # Maps root URL to home view
    path("fill/", include('fill.urls')),
    path("quiz/", include("quiz.urls")),
    path("management/", include("management.urls")),
    path("login/", include("login.urls")),
    path('compiler/', include('compiler.urls')),
    path('login/', include('django.contrib.auth.urls')),
]
