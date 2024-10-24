from django.urls import path
from catalog.views import view_catalog

app_name = 'catalog'

urlpatterns = [
    path('', view_catalog, name='view_catalog'),
    
]