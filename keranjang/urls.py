from django.urls import path
from . import views

app_name = 'keranjang'

urlpatterns = [
    path('', views.view_keranjang, name='view_keranjang'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout_page'),
    path('payment-successful/', views.payment_successful, name='payment_successful'),
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('update-quantity-ajax/', views.update_quantity_ajax, name='update_quantity_ajax'),
    path('remove-from-cart-ajax/', views.remove_from_cart_ajax, name='remove_from_cart_ajax'),]


