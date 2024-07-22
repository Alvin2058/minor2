# fill/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Exercise, Submission

def exercise_view(request, exercise_id=None):
    exercises = Exercise.objects.all().order_by('id')
    current_exercise = None
    next_exercise = None
    prev_exercise = None

    if exercise_id is None:
        current_exercise = get_object_or_404(Exercise, id=1)  # Default to the exercise with id 1
    else:
        current_exercise = get_object_or_404(Exercise, id=exercise_id)
    
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
