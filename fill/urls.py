# fill/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.exercise_view, name='home'),  
    path('fill/', views.exercise_view, name='fill_latest'),  # This load exercise with id 1 by default
    path('fill/<int:exercise_id>/', views.exercise_view, name='fill_specific'),  
    path('check_answer/', views.check_answer, name='check_answer'),
]
