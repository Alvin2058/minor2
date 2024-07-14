# fill/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # path('', views.exercise_view, name='home'),  
    path('fillex/', views.exercise_view, name='fill_latest'),  # This loads the latest exercise by default
    path('fill/<int:exercise_id>/', views.exercise_view, name='fill_specific'),  # This loads a specific exercise by ID
    path('check_answer/', views.check_answer, name='check_answer'),
]

