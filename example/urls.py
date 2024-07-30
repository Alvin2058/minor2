# example/main-urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Import views from the current directory

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name='home'),
    path("aboutus/", views.aboutus, name='aboutus'),
     path("contactus/", views.contactus, name='contactus'), # Maps root URL to home view
    path("fill/", include('fill.urls')),
    path("quiz/", include("quiz.urls")),
    path("login/", include("login.urls")),
    path('compiler/', include('compiler.urls')),
    path('login/', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
