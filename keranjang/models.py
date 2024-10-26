# models.py
from django.db import models

class Sneaker(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=200)
    release_date = models.DateField()
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class PurchaseHistory(models.Model):
    sneaker = models.ForeignKey('catalog.Sneaker', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.sneaker.price

    def __str__(self):
        return f"{self.quantity} x {self.sneaker.name} purchased by {self.user.username}"

