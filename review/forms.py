from django.forms import ModelForm
from review.models import Review
from django.utils.html import strip_tags


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review_description', 'rating']
    
    def clean_review_description(self):
        review_description = self.cleaned_data["review_description"]
        return strip_tags(review_description)