"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movie_reviews import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="home"),

    # Account registration and login/logout
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/login/", views.CustomLoginView.as_view(), name="login"),
    path("logout", views.LogoutView, name='logout'),

    # Account reviews - view, update, delete
    path("account/", views.AccountDisplayView.as_view(), name="account"),
    path("account_reviews", views.AccountReviewDisplayView.as_view(), name="account_reviews"),
    path("review_update/<pk>", views.AccountReviewUpdateView.as_view(), name="review_update"),
    path("review_delete/<pk>", views.AccountReviewDeleteView.as_view(), name="review_delete"),

    # All movies page
    path("all_movies/", views.FilterMovieView.as_view(), name="all_movies"),

    # Movie genres
    path("genres/", views.ShowAllGenres.as_view(), name="genres"),
    path("genres/<str:genre_name>", views.ShowGenreView.as_view(), name="show_genre"),

    # Search results page
    path("search_result/", views.SearchResultView.as_view(), name="search_result"),

    # Writing a review
    path("review/<str:movie_title>/", views.UserReviewView.as_view(), name="review"),
    path("review_done/", views.user_review_done_view, name="review_done"),

    # Account and password change
    path("account_pass_change/", 
         auth_views.PasswordChangeView.as_view(template_name="movie_reviews/account_pass_change.html"), name="account_password_change"),
    path("account_pass_change_done", 
         auth_views.PasswordChangeDoneView.as_view(template_name="movie_reviews/account_pass_done.html"), name="password_change_done"),

]

# Search bar functionality and results page 
# setup the api 