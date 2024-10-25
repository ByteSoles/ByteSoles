from django.urls import path
from detail_product.views import show_product, nyoba

app_name = 'detail_product'

urlpatterns = [
    path('product/<slug:slug>/', show_product, name='show_product'),
    path('', nyoba, name='nyoba')
]
