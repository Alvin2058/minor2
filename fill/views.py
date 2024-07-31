import random
from django.shortcuts import render
from django.http import JsonResponse
from .models import FillInTheBlankQuestion

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def random_fill_in_the_blank_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()
        question_id = request.POST.get('question_id')

        try:
            question = FillInTheBlankQuestion.objects.get(id=question_id)
        except FillInTheBlankQuestion.DoesNotExist:
            return JsonResponse({'result': 'Invalid question.'}, status=400)

        correct_answer = question.correct_answer.strip()

        if user_input == correct_answer:
            result = "Correct!"
        else:
            result = "Incorrect, try again."

        return JsonResponse({'result': result})

    subject = request.GET.get('subject')
    if subject:
        questions = FillInTheBlankQuestion.objects.filter(subject=subject)
        if questions.exists():
            question = random.choice(questions)
            return render(request, 'fill/fill_in_the_blank.html', {'question': question})
        else:
            return render(request, 'fill/no_questions.html')
    
    return render(request, 'fill/fill_in_the_blank.html', {'question': None})

def fetch_next_question(request):
    subject = request.GET.get('subject')
    if subject:
        questions = FillInTheBlankQuestion.objects.filter(subject=subject)
        if not questions.exists():
            return JsonResponse({'error': 'No more questions available.'}, status=404)

        question = random.choice(questions)
        question_data = {
            'id': question.id,
            'question_definition': question.question_definition,
            'question_text': question.question_text,
        }
        return JsonResponse(question_data)
    
    return JsonResponse({'error': 'Subject not provided.'}, status=400)

def fetch_hint(request):
    question_id = request.GET.get('question_id')
    try:
        question = FillInTheBlankQuestion.objects.get(id=question_id)
        hint = question.hint
        return JsonResponse({'hint': hint})
    except FillInTheBlankQuestion.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)
