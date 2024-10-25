from django.urls import path
from homepage.views import show_homepage, register, login_user, logout_user

app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]