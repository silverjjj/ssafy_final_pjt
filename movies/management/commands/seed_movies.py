from django.core.management.base import BaseCommand
# from . import _provider
from django_seed import Seed
import random
from movies.models import MovieRatings, Movie
from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()  # 모든 user를 가져옴
movies = Movie.objects.all()
point = [1,2,3,4,5,6,7,8,9,10]
class Command(BaseCommand):
    help = 'This command creates MovieRatings' 
    def add_arguments(self, parser): 
        parser.add_argument('--number', default=1, 
        type=int, help="How many MovieRatings do you want to create?")
    def handle(self, *args, **options):
        num = options.get('number')
        for _ in range(num):
            MovieRatings.objects.create(movie=random.choice(movies),rater=random.choice(users),score=random.choice(point))
