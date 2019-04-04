from django.urls import path
from .views import profile_home


urlpatterns = [
    path('me', profile_home, name="profile_home"),
]