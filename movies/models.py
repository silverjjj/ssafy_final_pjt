from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, null=True)
    release_date = models.DateField(auto_now=False, null=True)
    popularity = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    adult = models.BooleanField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    original_language = models.CharField(max_length=200, null=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')

    def __str__(self):
        return self.title

class Moviestore(models.Model):
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, null=True)
    release_date = models.DateField(auto_now=False, null=True)
    popularity = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    adult = models.BooleanField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    original_language = models.CharField(max_length=200, null=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='stored_movies')

    def __str__(self):
        return self.title

class MovieRatings(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    score = models.IntegerField()
    def __str__(self):
        return self.movie.title

class PleaseAdd(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    movie_request = models.CharField(max_length=200)

    def __str__(self):
        return self.movie_request

class MovieLine(models.Model):
    movie = models.CharField(max_length=150)
    line = models.TextField()

    def __str__(self):
        return self.movie
