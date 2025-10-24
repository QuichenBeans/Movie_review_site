from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    title = models.CharField(max_length=150)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True, default='2000-01-01')
    rating = models.CharField(max_length=100, blank=True) 
    rotten_tomatoes_rating = models.CharField(max_length=40, null=True)
    synopsis = models.TextField(blank=True)
    actors = models.CharField(max_length=100, null=True)
    runtime = models.CharField(max_length=100, null=True)
    awards = models.CharField(max_length=100, null=True)
    poster_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.title}"
    
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(blank=True) 
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'movie'], name='unique_movie_review')]
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.title} - {self.movie}"



