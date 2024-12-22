from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('json/', views.get_wishlist_json, name='get_wishlist_json'),
    path('add-to-wishlist-flutter/', views.add_to_wishlist_flutter, name='add_to_wishlist_flutter'),
]