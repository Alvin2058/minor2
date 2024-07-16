# my_app/urls.py
from django.urls import path
from .views import index, get_language_id

urlpatterns = [
    path('', index, name='compiler'),
    path('get_language_id/', get_language_id, name='get_language_id')
]