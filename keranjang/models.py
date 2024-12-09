# models.py
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Sneaker

class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_items = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)
    sneaker_name = models.CharField(max_length=255)
    sneaker_price = models.IntegerField(default=0)
    sneaker_image = models.URLField()
    quantity = models.IntegerField(default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.sneaker.name} purchased by {self.user.username}"