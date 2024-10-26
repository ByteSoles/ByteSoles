from django.urls import path
<<<<<<< HEAD
from homepage.views import view_homepage
=======
from homepage.views import show_homepage, register, login_user, logout_user
>>>>>>> 9e74df23bcf0cf31dab7e02d81e28a57a4733f71

app_name = 'homepage'

urlpatterns = [
<<<<<<< HEAD
    path('', view_homepage, name='view_homepage'),
    
=======
    path('', show_homepage, name='show_homepage'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
>>>>>>> 9e74df23bcf0cf31dab7e02d81e28a57a4733f71
]