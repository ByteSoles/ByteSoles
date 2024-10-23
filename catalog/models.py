from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255,db_index=True)
    slug = models.SlugField(max_length=255,unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

class SneakerManager(models.Manager):
    def get_queryset(self):
        return super(SneakerManager,self).get_queryset().filter(is_active= True)
    

class Sneaker(models.Model):
    
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.IntegerField()
    release_date = models.DateField()


    class Meta:
        verbose_name_plural = 'Sneaker'
        ordering = ['release_date']


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("store:sneaker_detail", args=[self.slug])
