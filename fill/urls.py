from django.urls import path
from . import views

urlpatterns = [
    path('fillex/', views.exercise_view, name='fill_latest'),  # Default to latest exercise
    path('fill/<str:subject>/', views.exercise_view, name='fill_subject'),  # Filter by subject
    path('fill/<int:exercise_id>/', views.exercise_view, name='fill_specific'),  # Specific exercise by ID
    path('check_answer/', views.check_answer, name='check_answer'),
]
