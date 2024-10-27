from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')), 
    path('catalog/', include('catalog.urls')),
    #path('catalog/products/<slug:product_slug>/', views.show_product_by_slug, name='sneaker_detail'),
    path('detail_product/', include('detail_product.urls')),
    path('keranjang/', include('keranjang.urls')),
    path('review/', include('review.urls')),
]
