from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Movie, Review
from .forms import CustomUserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

def index(request):
    return render(request, "movie_reviews/home.html")

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "movie_reviews/signup.html"


