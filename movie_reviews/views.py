from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .models import Movie, Review
from .filters import MovieFilter
from .forms import CustomUserCreationForm, AccountUpdateForm, ReviewMovieForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib import messages
import requests
from django.db.models import Q
from datetime import datetime

API_KEY = '8fdbb97b'

# Simple homepage render

def index(request):
    return render(request, "movie_reviews/home.html")

# Register, logging in and logout

class CustomLoginView(LoginView):
    template_name = "movie_reviews/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, "movie_reviews/home.html")
        return super().dispatch(request, *args, **kwargs)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "movie_reviews/signup.html"

def LogoutView(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return render(request, "movie_reviews/home.html")

# Account display, update details

class AccountDisplayView(LoginRequiredMixin, UpdateView):
    template_name = "movie_reviews/account.html"
    model = User
    form_class = AccountUpdateForm
    success_url = reverse_lazy("account")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def get_object(self, queryset=None):
        return self.request.user
    
class AccountReviewDisplayView(LoginRequiredMixin, ListView):
    model = Review
    template_name = "movie_reviews/account_reviews.html"
    paginate_by = 15
    context_object_name = "reviews"

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

# Review page  

class UserReviewView(LoginRequiredMixin, View):
    template_name = "movie_reviews/write_a_review.html"
    form_class =  ReviewMovieForm
    model = Review

    def get(self, request, movie_title):
        movie = get_object_or_404(Movie, title=movie_title)
        form = self.form_class()
        return render(request, self.template_name, {
            'movie': movie,
            'form': form
        })

    def post(self, request, movie_title):
        movie = get_object_or_404(Movie, title=movie_title)
        form = self.form_class(request.POST)

        if form.is_valid():
            if Review.objects.filter(user=request.user, movie=movie).exists():
                messages.error(self.request, "You have already reviewed this movie")
                return render(request, self.template_name, {
                    'movie': movie,
                    'form': form
                })
            
            review = form.save(commit=False)
            review.user = self.request.user
            review.movie = movie
            review.save()

            return redirect('review_done')
        
        return render(request, self.template_name, {
            'movie': movie,
            'form': form
        })

def user_review_done_view(request):
    messages.success(request, 'Review successfully created')
    return render(request, "movie_reviews/write_a_review_done.html")

# Updating and deleting review

class AccountReviewDeleteView(DeleteView):
    model = Review
    template_name = "movie_reviews/review_delete.html"
    success_url = reverse_lazy("account_reviews")

class AccountReviewUpdateView(UpdateView):
    model = Review
    template_name = "movie_reviews/review_update.html"
    success_url = reverse_lazy("account_reviews")
    form_class = ReviewMovieForm

# All movies page with filters (sort by 'title' for example)

class FilterMovieView(FilterView):
    model = Movie
    template_name = "movie_reviews/all_movies.html"
    paginate_by = 6
    filterset_class = MovieFilter

    def get_queryset(self):
        return Movie.objects.exclude(title__isnull=True).exclude(title='')

# Movie genres 

class ShowAllGenres(ListView):
    model = Movie
    template_name = "movie_reviews/genres/all_genres.html"
    context_object_name = "genres"

    def get_queryset(self):
        return Movie.objects.values_list('genre', flat=True).distinct()

class ShowGenreView(ListView):
    template_name = "movie_reviews/genres/show_genre.html"
    context_object_name = "movies"
    paginate_by = 6

    def get_queryset(self):
        self.genre_name = self.kwargs['genre_name']
        return Movie.objects.filter(genre__icontains=self.genre_name)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = self.genre_name.title()
        return context

# Search bar and attached api call - db save

class SearchResultView(ListView):
    model = Movie
    template_name = "movie_reviews/search_result.html"
    context_object_name = "results"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(genre__icontains=query) |
                Q(director__icontains=query) |
                Q(release_date__icontains=query) |
                Q(rating__icontains=query) |
                Q(synopsis__icontains=query) |
                Q(actors__icontains=query) |
                Q(runtime__icontains=query) |
                Q(awards__icontains=query) |
                Q(rotten_tomatoes_rating__icontains=query)
            )

            if not queryset.exists():
                api_url = f'http://www.omdbapi.com/?t={query}&apikey={API_KEY}'
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()

                    ratings = data.get('Ratings', '')
                    rotten_tomatoes_rating = None
                    for rating in ratings:
                        if rating.get('Source') == 'Rotten Tomatoes':
                            rotten_tomatoes_rating = rating.get('Value')
                            break

                    omdb_date = data.get('Released', '')
                    if omdb_date and omdb_date != 'N/A':
                        try:
                            release_date = datetime.strptime(omdb_date, '%d %b %Y').date()
                        except ValueError:
                            release_date = None
                    else:
                        release_date = None

                    movie, created = Movie.objects.update_or_create(
                        title = data.get('Title', ''),
                        defaults = {
                            'genre' : data.get('Genre', ''),
                            'director' : data.get('Director', ''),
                            'release_date' : release_date,
                            'rating' : data.get('imdbRating', ''),
                            'synopsis' : data.get('Plot', ''),
                            'actors' : data.get('Actors'),
                            'runtime' : data.get('Runtime'),
                            'awards' : data.get('Awards'),
                            'rotten_tomatoes_rating' : rotten_tomatoes_rating
                        }
                    ) 
                    queryset = Movie.objects.filter(id=movie.id)
                    
                    queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(genre__icontains=query) |
                    Q(director__icontains=query) |
                    Q(release_date__icontains=query) |
                    Q(rating__icontains=query) |
                    Q(synopsis__icontains=query) |
                    Q(actors__icontains=query) |
                    Q(runtime__icontains=query) |
                    Q(awards__icontains=query) |
                    Q(rotten_tomatoes_rating__icontains=query)
                    )

        return queryset.order_by('-release_date')




# API data retrieval - unsure if this is still needed

# def get_api_data(request):
#     api_url = f'http://www.omdbapi.com/?i=tt3896198&apikey={API_KEY}'
#     response = requests.get(api_url)
#     data = response.json()

#     title = data['Title']
#     genre = data['Genre']
#     director = data['Director']
#     release_date = data['Released']
#     rating = data['imdbRating']
#     synopsis = data['Plot']

#     Movie.objects.create(
#         title = title,
#         genre = genre,
#         director = director,
#         release_date = release_date,
#         rating = rating,
#         synopsis = synopsis
#     )








