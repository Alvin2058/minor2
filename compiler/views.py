import random
import requests
from django.http import JsonResponse
from django.shortcuts import render
from .forms import CodeForm
from .models import compiler_question

# Judge0 API URL and headers
L = "https://judge0-ce.p.rapidapi.com/submissions"
headers = {
    "Content-Type": "application/json",
    'x-rapidapi-key': "5e83683b33msh9c7c3f0797f6669p178722jsn54d596782374",
    'x-rapidapi-host': "judge0-ce.p.rapidapi.com"
}

def index(request):
    if request.method == 'POST':
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = CodeForm(request.POST)
            if form.is_valid():
                language = form.cleaned_data['language']
                code = form.cleaned_data['code']
                
                # Prepare the data for Judge0 API
                data = {
                    'source_code': code,
                    'language_id': get_language_id(language)
                }
                
                try:
                    response = requests.post(L, json=data, headers=headers)
                    response.raise_for_status()
                    
                    if response.status_code == 201:
                        token = response.json().get('token')
                        
                        if token:
                            # Check the status of the submission
                            result_url = f"{L}/{token}"
                            result_response = requests.get(result_url, headers=headers)
                            
                            # Handle the result JSON
                            if result_response.status_code == 200:
                                result_json = result_response.json()
                                return JsonResponse({
                                    
                                    'time': result_json.get('time'),
                                    'memory': result_json.get('memory'),
                                    'stdout': result_json.get('stdout'),
                                    'stderr': result_json.get('stderr'),
                                    
                                })
                            else:
                                return JsonResponse({'error': f"Failed to fetch result: {result_response.status_code}"}, status=400)
                        else:
                            return JsonResponse({'error': "Failed to get token from response"}, status=400)
                    else:
                        return JsonResponse({'error': f"Failed to submit code: {response.status_code}"}, status=400)
                
                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': f"Error during API request: {str(e)}"}, status=400)
            
            else:
                return JsonResponse({'error': "Form data is not valid"}, status=400)
        
        else:
            return JsonResponse({'error': "Invalid request type"}, status=400)
    
    else:
        form = CodeForm()
    
    try:
        question_object = compiler_question.objects.first()  # Retrieve the first question object
        question = question_object.questions if question_object else "Default Question Title"
    except compiler_question.DoesNotExist:
        question = "Default Question Title"

    return render(request, 'compiler/compiler.html', {'form': form, 'question': question})

def get_random_question(request):
    if request.method == 'GET':
        try:
            questions = compiler_question.objects.values_list('questions', flat=True)
            if questions:
                question = random.choice(questions)
                return JsonResponse({'question': question})
            else:
                return JsonResponse({'question': 'No questions available.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def get_language_id(language):
    language_map = {
        'python3': 71, # language_id for Python 3 in Judge0
        'cpp': 54,     # language_id for C++ in Judge0
        'java': 62,    # language_id for Java in Judge0
        'php': 63,     # language_id for PHP in Judge0
        'html': 68,    # language_id for HTML in Judge0
        'c': 50        # language_id for C in Judge0     
    }
    return language_map.get(language, 71)
