import requests
from django.shortcuts import render
import logging
from .forms import CodeForm

logger = logging.getLogger(__name__)

L = "https://judge0-ce.p.rapidapi.com/submissions"

headers = {
    "Content-Type": "application/json",
    'x-rapidapi-key': "5e83683b33msh9c7c3f0797f6669p178722jsn54d596782374",
    'x-rapidapi-host': "judge0-ce.p.rapidapi.com"
}
print("hello")

def index(request):
    if request.method == 'POST':
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
                 # Raise an exception for bad response status
                
                

                
                # Extract token if request was successful
                if response.status_code == 201:
                    token = response.json().get('token')
                    
                    if token:
                        # Check the status of the submission
                        result_url = f"{L}/{token}"
                        result_response = requests.get(result_url, headers=headers)
                        
                        # Handle the result JSON
                        if result_response.status_code == 200:
                            result_json = result_response.json()
                            time = result_json.get('time')
                            memory = result_json.get('memory')
                            stdout = result_json.get('stdout')
                            stderr = result_json.get('stderr')
                            compile_output = result_json.get('compile_output')
                            message = result_json.get('message')
                            
                            return render(request, 'compiler/compiler.html', {
                                'time': time,
                                'memory': memory,
                                'stdout': stdout,
                                'stderr': stderr,
                                'compile_output': compile_output,
                                'message': message,
                            })
                        else:
                            return render(request, 'compiler/compiler.html', {'error': f"Failed to fetch result: {result_response.status_code}"})
                    else:
                        return render(request, 'compiler/compiler.html', {'form': form, 'error': "Failed to get token from response"})
                else:
                    return render(request, 'compiler/compiler.html', {'form': form, 'error': f"Failed to submit code: {response.status_code}"})
            
            except requests.exceptions.RequestException as e:
                return render(request, 'compiler/compiler.html', {'form': form, 'error': f"Error during API request: {str(e)}"})
            
    else:
        form = CodeForm()
    
    return render(request, 'compiler/compiler.html', {'form': form})

def get_language_id(language):
    language_map = {
        'python3': 71, # language_id for Python 3 in Judge0
        'cpp': 54,     # language_id for C++ in Judge0
        'java': 62     # language_id for Java in Judge0
    }
    return language_map.get(language, 71)

