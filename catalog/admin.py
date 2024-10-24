from django.contrib import admin
from catalog.models import Sneaker
# Register your models here.

class SneakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'release_date')
    search_fields = ('name', 'brand')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
admin.site.register(Sneaker, SneakerAdmin)
