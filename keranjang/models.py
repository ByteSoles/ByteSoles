# models.py
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Sneaker  # Pastikan Sneaker diimpor dari app catalog
import json

class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_data = models.TextField(default='{}')  # Menyimpan data keranjang dalam format JSON

    def __str__(self):
        return f"Cart of {self.user.username}"

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.sneaker.price

    def __str__(self):
        return f"{self.quantity} x {self.sneaker.name} purchased by {self.user.username}"