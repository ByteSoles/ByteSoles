from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from catalog.models import Sneaker
import uuid

class Rating(models.Model):
    sneaker = models.OneToOneField(Sneaker, on_delete=models.CASCADE)
    rating = models.DecimalField(default=0, max_digits=5, decimal_places=1)

    def __str__(self):
        return str(self.pk)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    review_description = models.CharField(max_length=255)
    score = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )

    class Meta:
        unique_together = ('user', 'sneaker')

    def __str__(self):
        return f"{self.user.username} review of {self.sneaker.name}"