#main-urls.py
from django.contrib import admin
from django.urls import path,include
from example import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include("account.urls")),
    path("", views.home),  # Maps root URL to home views
    path("aboutus",views.aboutus),
    path("fill/",include('fill.urls')),
    path("quiz/", include("quiz.urls")),
    path("management/", include("management.urls")),
]
