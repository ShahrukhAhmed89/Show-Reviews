from django.urls import path
from .views import home, drama_page, paginate_reviews, save_review, add_review, toggle_likes, delete_review


urlpatterns = [
    path('', home, name="home"),
    path('<int:id>/<slug:slug>', drama_page, name="show_page"),
    path('paginate_reviews/<id>', paginate_reviews),
    path('save_review/', save_review),
    path('add_review/', add_review),
    # path('add_rating/', add_rating),
    path('toggle_likes/', toggle_likes),
    path('delete_review/', delete_review)
]