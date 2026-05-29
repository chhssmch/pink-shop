from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']

    def clean_rating(self): 
        rating = self.cleaned_data.get('rating') 
        if rating is not None and (rating < 1 or rating > 5): 
            raise forms.ValidationError("Оценка должна быть от 1 до 5 звезд!")
        return rating
