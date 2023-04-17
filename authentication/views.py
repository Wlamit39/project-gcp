from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
import json

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        User.objects.create(username=username, password=password)
        return JsonResponse({'message': 'Signup successful'})
    return JsonResponse({'message': 'Invalid request method'})