# profile/urls.py
from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('get_profile/', views.get_profile, name='get_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
]