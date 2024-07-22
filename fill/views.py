# fill/views.py

from django.shortcuts import render, get_object_or_404,render 
from django.http import JsonResponse
from .models import Exercise, Submission
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@login_required
def exercise_view(request, subject=None, exercise_id=None):
    if subject:
        exercises = Exercise.objects.filter(subject=subject)
    else:
        exercises = Exercise.objects.all()

    if exercise_id:
        current_exercise = get_object_or_404(exercises, id=exercise_id)
    else:
        current_exercise = exercises.first()

    next_exercise = exercises.filter(id__gt=current_exercise.id).first()
    prev_exercise = exercises.filter(id__lt=current_exercise.id).last()

    context = {
        'exercise': current_exercise,
        'next_exercise': next_exercise,
        'prev_exercise': prev_exercise,
    }
    return render(request, 'exercise.html', context)


def check_answer(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        exercise_id = request.POST.get('exercise_id')

        try:
            exercise = Exercise.objects.get(id=exercise_id)
            correct_answer = exercise.correct_answer

            # Validate the user's input
            if user_input == correct_answer:
                result = 'Correct!'
            else:
                result = 'Incorrect!'

            # Save submission record
            submission = Submission.objects.create(
                exercise=exercise,
                user_input=user_input,
                is_correct=(result == 'Correct!')
            )
            submission.save()

            # Prepare response data
            response_data = {
                'result': result,
                'definition': exercise.definition if result == 'Correct!' else ''
            }

            return JsonResponse(response_data)

        except Exercise.DoesNotExist:
            result = 'Error: Exercise not found.'
            return JsonResponse({'result': result}, status=404)

    return JsonResponse({'error': 'Invalid request method'})
