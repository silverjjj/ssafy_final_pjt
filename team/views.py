from django.shortcuts import render
from movies.models import PleaseAdd, MovieLine, MovieRatings
from random import *

# Create your views here.
def index(request):
    lines = MovieLine.objects.all()
    luckynum = randrange(0,len(lines)-1)
    goodline = lines[luckynum]

    if request.user.is_authenticated:
        # 사용자가 DB추가 요청한 영화들
        moviecnt = request.user.movieratings_set.count()
        requests = PleaseAdd.objects.filter(requester = request.user)
        requests_cnt = requests.count()
        cnt = 0
        reviews = request.user.review_set.all()
        for review in reviews:
            cnt += review.like_users.count()
        cnt += reviews.count()
        cnt += request.user.comment_set.count()
        # point = 리뷰수 + 리뷰에 받은 좋아요 수 + 자기가 단 코멘트 개수
        context =  {
            'cnt' : cnt,
            'requests': requests,
            'requests_cnt': requests_cnt,
            'goodline':goodline,
            'moviecnt':moviecnt,
        }
        return render(request, 'team/index.html', context)
    else:
        context = {
            'goodline':goodline,
        }
        return render(request, 'team/index.html', context)

def intro(request):
    return render(request, 'team/intro.html')

def myinfo(request):
    requests = PleaseAdd.objects.filter(requester = request.user)
    context = {
        'requests':requests,
    }
    return render(request, '')