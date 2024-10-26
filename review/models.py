from django.db import models
from catalog.models import Sneaker
import uuid

class Review(models.Model):
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    review_description = models.CharField(max_length=255)
    rating = models.FloatField()