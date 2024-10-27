from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    shoe_size = forms.IntegerField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ['shoe_size', 'address', 'phone_number']  # Sesuaikan dengan field yang ada di model Anda
