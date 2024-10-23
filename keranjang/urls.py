from django.urls import path
from keranjang.views import view_keranjang, add_to_cart, remove_from_cart

app_name = 'keranjang'

urlpatterns = [
    path('', view_keranjang, name='view_keranjang'),
    path('add/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]
