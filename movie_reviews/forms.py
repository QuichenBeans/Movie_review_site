from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Review


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class AccountUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        # Add first name and last name to the custom form and then add them as fields to change below
        fields = ("username", "email")

class ReviewMovieForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("title", "rating", "comment")
        widgets = {
            "rating": forms.NumberInput(attrs={
                "min": 1,
                "max": 10,
                "class": "form-control",
                "placeholder": "Rate between 1 and 10"
            }),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter review title"
            }),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write your review here...",
                "rows": 4
            })
        }
    
    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating < 1 or rating > 10:
            raise forms.ValidationError("Rating must be between 1 and 10.")
        return rating
