from django.urls import path
from catalog.views import view_catalog, get_product_json, get_filtered_products, product_detail, get_product_by_id
from detail_product.views import show_product, get_recently_viewed

app_name = 'catalog'

urlpatterns = [
    path('', view_catalog, name='view_catalog'), 
    path('view-json/', get_product_json, name='get_product_json'),
    path('get_filtered_products/', get_filtered_products, name='get_filtered_products'),
    path('products/<slug:product_slug>/', show_product, name='show_product'),
    path('recently_viewed/', get_recently_viewed, name='get_recently_viewed'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product_id/<int:id>/', get_product_by_id, name='get_product_by_id'), 
]
