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