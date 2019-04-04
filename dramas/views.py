from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from .models import Show
from reviews.models import Reviews
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils.html import linebreaks, escape
import json
from django.core.exceptions import PermissionDenied
from .forms import UserReviewForm
import requests
from django.contrib.auth.decorators import login_required






def home(request):
    # Queries for Home Page are generated and written to template by the script Creator.py
    return render(request, "home.html", {})

import time

def drama_page(request, id, slug):
    user_review = None
    start_time = time.time()

    show_details =get_object_or_404(Show, id=id)
   

    # start_time = time.time()

    # show_detail = requests.get('https://api.themoviedb.org/3/movie/550?api_key=366df131f29b8af650347fec8d0e315e&append_to_response=credits').json()
    # print("--- %s seconds ---" % (time.time() - start_time))


    reviews = show_details.reviews_set.prefetch_related('user') #show_details.reviews_set.prefetch_related('user', 'user_many_likes') #show_details.reviews_set.prefetch_related('user')
    rating = reviews.aggregate(Avg('rating'))
    count = reviews.count()

    if request.user.is_authenticated:
        try:
            user_review = Reviews.objects.get( show__id = id, user = request.user.chingu )  
        except:
            pass
        else:
            reviews = reviews.exclude(user = request.user.chingu)
    reviewSet = reviews.filter(has_post=True)[0:15]  #.annotate(like_count=Count('user_many_likes')).order_by('-like_count')[0:15]
    context = {
        "show"          : show_details,
        "reviews"       : reviewSet,
        "rating"        : rating,
        "count"         : count,
        "user_review"   :user_review,
    }
    return render(request, "show_page.html", context)

def save_review(request):
    if request.method == "POST":
        deserialize = json.loads(request.body)
        incoming_data = {
            'post'    : deserialize['post'].strip(),
            'rating'  : float(deserialize['rating'])   
        }
        review = get_object_or_404(Reviews, id=deserialize['id'])
        form = UserReviewForm(incoming_data, instance=review)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return JsonResponse({'response': linebreaks(escape(post.post))})
        else:
            return JsonResponse({'response': form.errors()})
    raise PermissionDenied





def add_review(request):
    if request.method == "POST":
        deserialize = json.loads(request.body)
        incoming_data = {
            'rating' : float(deserialize['rating']),
            'post'   : deserialize['post'].strip(),
        }
        show = get_object_or_404(Show, id=deserialize['id'])
        form = UserReviewForm(incoming_data)
        if form.is_valid():
            post = form.save(commit=False)
            if incoming_data['post']:
                post.has_post = True
            else:
                post.has_post = False
            post.show = show
            post.user = request.user.chingu
            post.save()
            return JsonResponse({'newReviewID': post.id})
        else:
            return JsonResponse({'response': form.errors()})
    raise PermissionDenied


@login_required(login_url='/login/')
def toggle_likes(request):
    user_action = None
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        user = request.user.chingu.id
        review = get_object_or_404(Reviews, id=deserialize['reviewId'])
        if user in review.user_likes:
            review.user_likes.remove(user)
            user_action = 0
        else:
            review.user_likes.append(user)
            user_action = 1
        review.save()
        return JsonResponse({'userAction':user_action})
    raise PermissionDenied




def delete_review(request):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        id = deserialize['id']
        print (deserialize)
        post = get_object_or_404(Reviews, id=id)
        post.delete()
        return JsonResponse({"message": 'deleted'})
    raise PermissionDenied

def paginate_reviews(request, id):
    check_post_likes = False
    if request.method == 'GET':
        review_list = Reviews.objects.filter(show__id=id, has_post=True).prefetch_related('user')
        paginate_reviews = []
        paginator = Paginator(review_list, 15)
        page = request.GET.get('page')
        reviews = paginator.get_page(page)
        for review in reviews:
            has_user_liked_post = 'false'
            review_data = {
                "user"      : review.user.custom_username,
                "avatar"    : review.user.avatar.url,
                "post"      : linebreaks(escape(review.post)),
                "user_like" : has_user_liked_post,
                "rating"    : str(review.rating),
                "likes"     : len(review.user_likes) if review.user_likes else 0
            }
            paginate_reviews.append(review_data)
        return JsonResponse({'paginated_reviews': json.dumps(paginate_reviews), 'next_page': reviews.has_next()})
    raise PermissionDenied



# Create your views here.

    # user_review = None
    # show_details = Show.objects.get(id=id)
    # if request.user.is_authenticated:
    #     try:
    #         user_review = Reviews.objects.get( show__id = id, user = request.user.chingu )
    #     except:
    #         reviews = show_details.reviews_set.prefetch_related('user')
    #     else:
    #         reviews = show_details.reviews_set.exclude(user = request.user.chingu).prefetch_related('user')
    #     #user_review = reviews.filter( user=request.user.chingu )[0]
    #     # if reviews.filter(id=user_review.id).exists():
    #     #     reviews.exclude(id=user_review.id)
    # else:
    #     reviews = show_details.reviews_set.prefetch_related('user')
    # rating = reviews.aggregate(Avg('rating'))
    # count = reviews.count()
    #user_review = reviews.filter( user=request.user.chingu )[0]
    # if reviews.filter(id=user_review.id).exists():
    #     reviews.exclude(id=user_review.id)
    

    # user_review = Reviews.objects.filter( show__id=id).filter( user=request.user.chingu )

    # show_details.reviews_set.annotate(like_count=Count('user_many_likes')).order_by('-like_count')



# def add_review(request):
#     if request.method == "POST":
#         deserialize = json.loads(request.body)
#         incoming_data = {
#             'post'      : deserialize['post'],
#             'rating'    : deserialize['rating']
#         }

#         review = Reviews.objects.get(show__id=1, user = request.user.chingu)
#         print (incoming_data)
#         form = UserReviewForm(incoming_data, instance=review)
#         if form.is_valid():
#             # form.save()
#             post = form.save(commit=False)
#             # post.save()
#         # # review = Reviews.objects.get(id=id)
#         # print (form.is_valid())
#         # if form.is_valid():
#         #     post = form.save(commit=False)
#         #     post.save()
#             return JsonResponse({'response': post.post})
#         return JsonResponse({'response': form.errors})
