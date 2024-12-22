from django.urls import path
from keranjang.views import checkout, update_quantity_ajax, remove_from_cart_ajax, get_user_cart, add_to_cart,view_keranjang, show_json, show_xml, show_json_by_id, show_xml_by_id,remove_from_cart_ajax_flutter,add_to_cart_flutter
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'keranjang'

urlpatterns = [
    path('', view_keranjang, name='view_keranjang'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout_page'),
    path('update-quantity-ajax/', update_quantity_ajax, name='update_quantity_ajax'),
    path('remove-from-cart-ajax/', remove_from_cart_ajax, name='remove_from_cart_ajax'),
    path('remove-from-cart-ajax-flutter/', remove_from_cart_ajax_flutter, name='remove_from_cart_ajax_flutter'),
    path('get-user-cart/', get_user_cart, name='get_user_cart'),
    path('homepage/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('add-to-cart-flutter/', add_to_cart_flutter, name='add_to_cart_flutter'),
    ]