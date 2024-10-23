from django.contrib import admin
from django.urls import path, include  # include is necessary for app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('keranjang/', include('keranjang.urls')),  # Make sure this line matches the app name and file location
]
