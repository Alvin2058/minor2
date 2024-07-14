from django.shortcuts import render, redirect
from django.views import View
from .models import Question, Mark
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from random import sample

# Create your views here.

class Quiz(View):
    def get(self, request):
        subject = request.GET.get('subject', None)  # Get subject from query parameter
        if subject:
            questions = list(Question.objects.filter(verified=True, subject=subject))
        else:
            questions = list(Question.objects.filter(verified=True,subject=subject))
        
        random_questions = sample(questions, len(questions))
        return render(
            request,
            "quiz/quiz.html",
            {"questions": random_questions, "subject": subject}  # Pass subject to template
        )

    def post(self, request):
        User = get_user_model()  # Retrieve the User model
        user_instance = User.objects.get(username=request.user.username)  # Get the User instance

        mark = Mark(user=user_instance, total=Question.objects.filter(verified=True).count())
        correct_answers = []
        incorrect_answers = []

        for i in range(1, mark.total + 1):
            q_id = request.POST.get(f"q{i}", None)
            selected_option = request.POST.get(f"q{i}o", None)
            q = Question.objects.filter(pk=q_id, verified=True).first()
            if q:
                if selected_option == q.correct_option:
                    mark.got += 1
                    correct_answers.append(q)
                else:
                    incorrect_answers.append(q)

        mark.save()
        return render(request, "quiz/result.html", {
            "mark": mark,
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers
        })

#@method_decorator(login_required, name="dispatch")
class Result(View):
    def get(self, request):
        results = Mark.objects.filter(user=request.user)
        return render(request, "quiz/result.html", {"results": results})

class Leaderboard(View):
    def get(self, request):
        return render(
            request, 
            "quiz/leaderboard.html", 
            {"results": Mark.objects.all().order_by("-got")[:10]}
        )