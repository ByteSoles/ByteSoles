from django.urls import path
from homepage.views import show_homepage, register, logout_user
from homepage.views import view_homepage
from homepage.views import show_homepage, register, login_user, logout_user

app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('', view_homepage, name='view_homepage'),
    

]