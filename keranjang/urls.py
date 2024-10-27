from django.urls import path
from keranjang.views import checkout ,remove_from_cart,update_quantity,update_quantity_ajax,remove_from_cart_ajax,add_to_cart,view_keranjang
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'keranjang'

urlpatterns = [
    path('', view_keranjang, name='view_keranjang'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
    path('checkout', checkout, name='checkout_page'),
    path('update-quantity/<slug:slug>/', update_quantity, name='update_quantity'),
    path('update-quantity-ajax/', update_quantity_ajax, name='update_quantity_ajax'),
    path('remove-from-cart-ajax/', remove_from_cart_ajax, name='remove_from_cart_ajax'),
    ]