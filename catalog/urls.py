from django.urls import path
from catalog.views import view_catalog, get_product_json, get_filtered_products

app_name = 'catalog'

urlpatterns = [
    path('', view_catalog, name='view_catalog'),
    path('view-json/', get_product_json, name='get_product_json'),
    path('get_filtered_products/', get_filtered_products, name='get_filtered_products'),

    
]