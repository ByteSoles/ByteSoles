from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')), 
    path('catalog/', include('catalog.urls')),
    path('detail_product/', include('detail_product.urls')),
    path('keranjang/', include('keranjang.urls')),
    path('review/', include('review.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('profile/', include('user_profile.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

