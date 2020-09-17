from django.contrib import admin
from .models import Genre, Movie, MovieLine,MovieRatings, Moviestore

# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieRatings)
admin.site.register(MovieLine)
admin.site.register(Moviestore)