# quiz/views.py
from django.shortcuts import render, redirect
from django.views import View
from .models import Question, Mark, AttemptedQuestion
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from random import sample
from django.contrib.auth import get_user_model
from django.db.models import Sum

@method_decorator(login_required, name='dispatch')
class Quiz(View):
    def get(self, request):
        user = request.user
        subject = request.GET.get('subject', None)  # Get subject from query parameter

        attempted_questions = AttemptedQuestion.objects.filter(user=user).values_list('question_id', flat=True)
        questions = Question.objects.exclude(id__in=attempted_questions)

        if subject:
            questions = questions.filter(subject=subject)
            # If no questions for the subject, show a message
            if not questions.exists():
                messages.info(request, f'No questions available for the subject: {subject}')
                return redirect('quiz')  # Redirect to quiz page or a suitable page

            questions = list(questions.order_by('?')[:10]) 
        else:
            questions = list(questions.order_by('?')[:10])  

        if not questions:
            return render(request, "quiz/quiz.html", {"questions": [], "subject": subject})

        # Sample requires a sequence, so convert to a list explicitly
        random_questions = sample(questions, len(questions))

        return render(request, "quiz/quiz.html", {"questions": random_questions, "subject": subject})

    def post(self, request):
        user_instance = request.user
        total_questions = 10
        mark = Mark(user=user_instance, total=total_questions)
        correct_answers = []
        incorrect_answers = []
        got = 0  # Initialize got count

        for key, value in request.POST.items():
            if key.startswith('q_id_'):  # Check for keys starting with 'q_id_'
                q_id = key.split('_')[-1]  # Extract question ID from key
                selected_option = request.POST.get(f'q_answer_{q_id}')  # Get selected answer based on question ID
                q = Question.objects.filter(pk=q_id).first()
                if q:
                    AttemptedQuestion.objects.create(user=user_instance, question=q)  # Log the attempted question
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
        if not request.user.is_authenticated:
            messages.info(request, 'You need to log in to take the quiz.')
            return redirect('login')  # Redirect to login page if not authenticated
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name="dispatch")
class History(View):
    def get(self, request):
        user_instance = request.user
        history = Mark.objects.filter(user=user_instance).order_by('-timestamp')
        return render(request, "quiz/history.html", {"history": history})

class Result(View):
    @method_decorator(login_required)
    def get(self, request, subject=None):
        user_instance = request.user
        total_questions = Question.objects.filter(subject=subject).count() if subject else Question.objects.count()
        results = Mark.objects.filter(user=user_instance, total=total_questions)
        return render(request, "quiz/result.html", {
            "results": results,
            "total_questions": total_questions,
            "subject": subject
        })

class Leaderboard(View):
    def get(self, request):
        # Aggregate total questions and total score for each user
        user_scores = Mark.objects.values('user').annotate(
            total_questions=Sum('total'),
            total_scored=Sum('got')
        ).order_by('-total_scored')[:10]

        # Fetch user instances to display usernames
        user_ids = [score['user'] for score in user_scores]
        users = {user.id: user for user in get_user_model().objects.filter(id__in=user_ids)}

        # Prepare data for rendering
        top_scores = []
        for score in user_scores:
            user = users.get(score['user'])
            top_scores.append({
                'username': user.username if user else 'Unknown',
                'total_questions': score['total_questions'],
                'total_scored': score['total_scored'],
            })

        return render(request, "quiz/leaderboard.html", {"top_scores": top_scores})
