from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from reviews.models import Reviews

# Create your views here.

def profile_home(request):
    reviews = Reviews.objects.filter(user=request.user.chingu).prefetch_related('show')
    context = {
        'reviews': reviews
    }
    print (reviews)
    return render(request, 'user_profile.html', context)