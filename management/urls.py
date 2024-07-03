from django.urls import path
from . import views

urlpatterns = [
    path("", views.Manage.as_view(), name="manage"),
    path("add_questions", views.AddQuestion.as_view(), name="add_question"),
]