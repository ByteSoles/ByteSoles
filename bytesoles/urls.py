"""
URL configuration for bytesoles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from homepage import views as homepage_views  # Sesuaikan dengan struktur proyek Anda
from login_regis import views as login_views  # Tambahkan ini


urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include('login_regis.urls')),
    path('login/', login_views.login_view, name='login'),  # Tambahkan ini
    path('register/', login_views.register_view, name='register'),  # Tambahkan ini juga jika diperlukan
    path('', homepage_views.view_homepage, name='view_homepage'),  # Perhatikan name di sini
    path('catalog/', include('catalog.urls')),
<<<<<<< HEAD
    path('detail_product/', include('detail_product.urls')),
    
=======
    path('review/', include('review.urls')),
>>>>>>> 9e74df23bcf0cf31dab7e02d81e28a57a4733f71
]
