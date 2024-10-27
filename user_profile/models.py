from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shoe_size = models.FloatField(null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)  # Mengizinkan nilai null dan blank
    
    def __str__(self):
        return self.user.username


for receiver in post_save.receivers:
    if receiver[0][0].__name__ in ['create_user_profile', 'save_user_profile']:
        post_save.disconnect(receiver=receiver[0][0], sender=User)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shoe_size = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
