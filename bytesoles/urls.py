from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path('admin/', admin.site.urls),
    path('keranjang/', include('keranjang.urls')),  # Make sure this line matches the app name and file location
    path('', include('homepage.urls')), 
    path('catalog/', include('catalog.urls')),
    path('detail_product/', include('detail_product.urls')),
    path('keranjang/', include('keranjang.urls', namespace='keranjang')),

    
]
