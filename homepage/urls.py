from django.urls import path
from homepage.views import view_homepage

app_name = 'homepage'

urlpatterns = [
    path('', view_homepage, name='view_homepage'),
    
]