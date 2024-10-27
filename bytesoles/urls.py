from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Tambahkan baris ini


urlpatterns = [

    path('admin/', admin.site.urls),
    path('keranjang/', include('keranjang.urls')),  # Make sure this line matches the app name and file location
    path('', include('homepage.urls')), 
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('detail_product/', include('detail_product.urls')),
    path('keranjang/', include('keranjang.urls', namespace='keranjang')),
    path('review/', include('review.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('profile/', include('user_profile.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),




]
