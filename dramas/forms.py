from django import forms
from reviews.models import Reviews

class UserReviewForm(forms.ModelForm):
    post = forms.CharField(required=False)

    class Meta:
        model = Reviews
        fields = ('rating', 'post',)