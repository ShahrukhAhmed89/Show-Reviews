from django.urls import path
from .views import user_feedback


urlpatterns = [
    path('user_feedback', user_feedback, name="user_feedback"),
]