#quiz urls.py
from django.urls import path
from .views import Leaderboard, UserHistory
from . import views

urlpatterns = [
    path("", views.Quiz.as_view(), name="quiz"),
    #path("add_question/", views.AddQuestion.as_view(), name="add_question"),
    path('history/', views.History.as_view(), name='history'),
    path("result/", views.Result.as_view(), name="result"),
    path("leaderboard/", views.Leaderboard.as_view(), name="leaderboard"),
    path('history/<int:user_id>/', UserHistory.as_view(), name='user_history'),
]