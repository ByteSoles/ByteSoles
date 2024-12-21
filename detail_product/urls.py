from django.urls import path
from detail_product.views import show_product, add_comment, get_comments

app_name = 'detail_product'

urlpatterns = [
    path('product/<slug:product_slug>/', show_product, name='show_product'),
    path('product/<slug:product_slug>/comments/', get_comments, name='get_comments'),
    path('product/<slug:product_slug>/add_comment/', add_comment, name='add_comment'),
]
