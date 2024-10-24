from django.urls import path
from review.views import show_reviews

app_name = 'review'

urlpatterns = [
    path('', show_reviews, name='show_reviews'),
]