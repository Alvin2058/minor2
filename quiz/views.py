# quiz views
from django.shortcuts import render, redirect
from django.views import View
from .models import Question, Mark
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from random import sample


@method_decorator(login_required, name='dispatch')
class Quiz(View):
    def get(self, request):
        subject = request.GET.get('subject', None)  # Get subject from query parameter
        
        questions = list(Question.objects.filter(subject=subject).order_by('?')[:10])
        
        random_questions = sample(questions, len(questions))
        
        return render(
            request,
            "quiz/quiz.html",
            {"questions": random_questions, "subject": subject}  # Pass subject to template
        )

    def post(self, request):
        user_instance = request.user  
        subject = request.GET.get('subject', None)  # Get subject from query parameter
        
        total_questions = 10
        
        mark = Mark(user=user_instance, total=total_questions)
        correct_answers = []
        incorrect_answers = []
        got = 0  # Initialize got count

        for key, value in request.POST.items():
            if key.startswith('q_id_'):  # Check for keys starting with 'q_id_'
                q_id = key.split('_')[-1]  # Extract question ID from key
                selected_option = request.POST.get(f'q_answer_{q_id}')  # Get selected answer based on question ID
                q = Question.objects.filter(pk=q_id, verified=True).first()
                if q:
                    selected_option_text = ""
                    if selected_option == 'A':
                        selected_option_text = q.option1
                    elif selected_option == 'B':
                        selected_option_text = q.option2
                    elif selected_option == 'C':
                        selected_option_text = q.option3
                    elif selected_option == 'D':
                        selected_option_text = q.option4
                    if selected_option == q.correct_option:
                        got += 1  # Increment got count for correct answers
                        correct_answers.append({
                            'question': q,
                            'selected_option': selected_option_text,
                            'correct_answer': q.c_answer,
                        })
                    else:
                        incorrect_answers.append({
                            'question': q,
                            'selected_option': selected_option_text,
                            'correct_answer': q.c_answer,
                        })
        
        mark.got = got  # Assign the calculated got count to mark object
        mark.save()
        
        return render(request, "quiz/result.html", {
            "mark": mark,
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers,
        })
    def dispatch(self, request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.info(request, 'You need to log in to take the quiz.')
            return redirect('login')  # Redirect to login page if not authenticated
        return super().dispatch(request, *args, **kwargs)

    
#@method_decorator(login_required, name="dispatch")

class Result(View):
    def get(self, request, subject=None):
        user_instance = request.user
        
        if subject:
            # Filter questions and count total for the specific subject
            total_questions = Question.objects.filter(subject=subject).count()
            # Retrieve mark instance for the specific subject
            results = Mark.objects.filter(user=user_instance, total=total_questions)
        # else:
            # If no subject specified, show total marks for all questions
            # total_questions = Question.objects.count()
            # results = Mark.objects.filter(user=user_instance, total=total_questions)
        
        return render(request, "quiz/result.html", {
            "results": results,
            "total_questions": total_questions,
            "subject": subject  # Pass subject to template for display purposes
        })


class Leaderboard(View):
    def get(self, request):
        return render(
            request, 
            "quiz/leaderboard.html", 
            {"results": Mark.objects.all().order_by("-got")[:10]}
        )