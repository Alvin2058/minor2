# urls.py
from django.urls import path
from .views import random_fill_in_the_blank_view, fetch_next_question, fetch_hint

urlpatterns = [
    path('random_question/', random_fill_in_the_blank_view, name='random_fill_in_the_blank'),
    path('random_question/next/', fetch_next_question, name='fetch_next_question'),
    path('random_question/hint/', fetch_hint, name='fetch_hint'),
]
