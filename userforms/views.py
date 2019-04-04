from django.shortcuts import render
from .forms import FeedbackForm
from django.core.exceptions import PermissionDenied
import json
from django.http import JsonResponse


# Create your views here.

def user_feedback(request):
    if request.method == "POST":
        deserialize = json.loads(request.body)
        incoming_data = {
            'problem' : deserialize['problem'],
            'text'   : deserialize['text'],
        }
        form = FeedbackForm(incoming_data)
        if form.is_valid:
            form.save()
            return JsonResponse({'response': 'saved'})
        else:
            return JsonResponse({'response': 'error'})
    else:
        raise PermissionDenied