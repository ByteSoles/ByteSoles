from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 
from django.conf import settings
from django.conf.urls.static import static
from user_profile.views import delete_account


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')), 
    path('catalog/', include('catalog.urls')),
    path('detail_product/', include('detail_product.urls')),
    path('keranjang/', include('keranjang.urls')),
    path('review/', include('review.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('user_profile/', include('user_profile.urls')),
    path('user_profile/delete_account/', delete_account, name='delete_account'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('authentication/', include('authentication.urls')),
    path('auth/', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)