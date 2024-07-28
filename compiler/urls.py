# my_app/urls.py
from django.urls import path
from .views import index, get_language_id,get_random_question

urlpatterns = [
    path('', index, name='compiler'),
    path('random-question/', get_random_question, name='get_random_question'),
    path('get_language_id/', get_language_id, name='get_language_id')
]