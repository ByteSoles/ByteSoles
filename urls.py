# user_profile/urls.py
from django.urls import path
from .views import update_personal_info, update_shipping_info

urlpatterns = [
    path('update_personal_info/', update_personal_info, name='update_personal_info'),
    path('update_shipping_info/', update_shipping_info, name='update_shipping_info'),
]

# wishlist/urls.py
from django.urls import path
from .views import add_to_wishlist, remove_from_wishlist

urlpatterns = [
    path('add/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/', remove_from_wishlist, name='remove_from_wishlist'),
]
