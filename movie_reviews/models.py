from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Movie(models.Model):
    api_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=50)
    genre = models.CharField(max_length=30)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.release_date.year})"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True) 
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'movie'], name='unique_movie_review')]
        ordering = ["-date_created"]


