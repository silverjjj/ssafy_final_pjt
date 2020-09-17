from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages

from random import *
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Movie, MovieRatings, Moviestore,Genre
from .serializers import MovieSerializer
from .forms import PleaseAddForm, RateForm, MoviestoreForm


# 영화 메인화면 - 몇가지 추천 영화들 선보이기
def index(request):
    # 평점순 + 사람들이 많이 봄
    movies_rate = Movie.objects.filter(vote_average__gte=8.5).order_by('-vote_count')[:12]
    # 대중성
    movies_popular = Movie.objects.order_by('-popularity')[:12]
    # 한국영화 + 대중성
    movies_korea = Movie.objects.filter(original_language='ko').order_by('-popularity')[:12]
    # 오늘의 영화 : 평점 8 넘으면서, vote_count>= 4000, 최신순 정렬
    movies_recommend = Movie.objects.filter(vote_average__gte=8, vote_count__gte=4000).order_by('-release_date')
    genre = {
        "Adventure":12, "Fantasy":14, "Animation":16, "Drama":18, "Horror":27, "Action":28, 
        "Comedy":35, "History":36, "Western":37, "Thriller":53, "Crime":80, "Documentary":99, 
        "Science Fiction":878, "Mystery":9648, "Music":10402, "Romance":10749, "Family":10751, "War":10752, 
        "TV Movie":10770, 
    }
    # 장르별로 영화 하나 추천 -  대중성 면에서
    movies_genre = []
    for key, value in genre.items():
        movie = Movie.objects.filter(genres=value).order_by('-popularity')[0]
        movies_genre.append([movie,key])
        
    movie_num = randrange(0,80)
    choice = movies_recommend[movie_num]

    choice_genre = []
    c_genres = choice.genres.all()
    for value in c_genres.values():
        choice_genre.append(value)

    context = {
        'movies_rate' : movies_rate,
        'movies_popular' : movies_popular,
        'movies_korea' : movies_korea,
        'movies_genre' : movies_genre,
        'choice' : choice,
        'choice_genre':choice_genre,
    }
    return render(request, 'movies/index.html', context)

# 영화 상세보기
def m_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    count = movie.like_users.count()
    if request.user.is_authenticated:
        ratings = MovieRatings.objects.filter(rater=request.user, movie=movie)
        r = False
        if ratings:
            r = True
        context = {
            'count': count,
            'movie': movie,
            'r':r
        }
        return render(request, 'movies/m_detail.html', context)
    else:
        context = {
            'count': count,
            'movie': movie,
        }
        return render(request, 'movies/m_detail.html', context)

# 박스오피스 받아오기
import urllib.request as ul
import json
import datetime
from final.settings import BOXOFFICE_API_KEY

#박스오피스
def boxoffice(request):
    today = datetime.date.today()
    dd = today.strftime('%Y%m%d').split('-')
    day = int(dd[0]) - 1

    url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={BOXOFFICE_API_KEY}&targetDt={day}"
    req = ul.Request(url)

    response = ul.urlopen(req)
    rescode = response.getcode()
    if(rescode == 200):
        responseData = response.read()
    result = json.loads(responseData)
    # print(result)
    movies = result['boxOfficeResult']['dailyBoxOfficeList']
    context = {
        'movies':movies,
    }
    return render(request, 'movies/boxoffice.html', context)

# 검색하는 페이지로 이동
def find(request):
    return render(request, 'movies/find.html')

# 검색결과 보여주는 페이지
def find2(request):
    b = request.GET.get('b','') # GET request의 인자중에 b 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if b: # b에 값이 들어있으면 true
        movies = Movie.objects.filter(Q(title__contains=b) | Q(original_title__contains=b)) 
    else:
        movies = '검색어와 일치하는 결과가 없습니다.'
    context = {
        'keyword':b,
        'movies': movies,
    }
    return render(request, 'movies/findresult.html', context)
 
# 일반 이용자가 영화DB 추가 요청
def please(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PleaseAddForm(request.POST)
            if form.is_valid():
                please = form.save(commit=False)
                please.requester = request.user
                please.save()
                return render(request, 'movies/find.html')
        else:
            form = PleaseAddForm()
        context = {
            'form':form,
        }
        return render(request, 'accounts/form.html', context)
    else:
        return redirect('accounts:login')

# 영화 좋아요
def movie_like(request, movie_pk):
    if request.user.is_authenticated:
        user = request.user # 현재 로그인한 유저
        movie = get_object_or_404(Movie, pk=movie_pk)

        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user) # 좋아요 취소
            liked = False
        else:
            movie.like_users.add(user) # 좋아요!
            liked = True
        count = movie.like_users.count()
        data = {
            'liked':liked,
            'count':count,
        }
        return JsonResponse(data)

def rate(request, movie_pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            m = get_object_or_404(Movie, pk=movie_pk)
            form = RateForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.rater = request.user
                rating.movie = m
                rating.save()
                new_vote_average = (float(m.vote_average * m.vote_count) + rating.score) / (m.vote_count)
                new_vote_average = round(new_vote_average,1)
                m.vote_count = m.vote_count + 1
                m.vote_average = new_vote_average
                m.save()
                return redirect('movies:m_detail', movie_pk)
        else:
            form = RateForm()
        context = {
            'form' : form
        }
        return render(request, 'movies/forms.html', context)
    else:
        return redirect('accounts:login')

def rate_update(request, movie_pk):
    if request.user.is_authenticated:
        m = get_object_or_404(Movie, pk=movie_pk)
        ratedata = MovieRatings.objects.get(rater=request.user, movie=m)
        num = ratedata.score
        if request.method == "POST":
            form = RateForm(request.POST, instance = ratedata)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.rater = request.user
                rating.movie = m
                rating.save()
                # 평점에 반영
                new_vote_average = (float(m.vote_average * m.vote_count) + (rating.score-num)) / (m.vote_count)
                new_vote_average = round(new_vote_average,1)
                m.vote_average = new_vote_average
                m.save()
                return redirect('movies:m_detail', movie_pk)
        else:
            form = RateForm(instance=ratedata)
        context = {
            'form' : form
        }
        return render(request, 'movies/forms.html', context)
    else:
        return redirect('accounts:login')

def rate_delete(request, movie_pk):
    if request.user.is_authenticated:
        m = get_object_or_404(Movie, pk=movie_pk)
        ratedata = MovieRatings.objects.get(rater=request.user, movie=m)
        # 기존 DB에서 이 평점의 영향 삭제
        total = (m.vote_average)*(m.vote_count)
        total -= ratedata.score
        m.vote_count -= 1
        m.vote_average = round(total/(m.vote_count),1)
        m.save()
        ratedata.delete()
        return redirect('movies:m_detail', movie_pk)
    else:
        return redirect('accounts:login')


# 추천 메인
def recommendation(request):
    num = randrange(0,499)
    # 무작위 추천
    movies1 = Movie.objects.order_by('-vote_count')[:500]
    randomone = movies1[num]
    # 괜찮은 추천
    movies2 = Movie.objects.filter(vote_count__gte=2000, vote_average__gte=8)
    many = movies2.count()
    num2 = randrange(0,many-1)
    notbadone = movies2[num2]
    context = {
        'random':randomone,
        'notbad':notbadone,
    }

    return render(request, 'movies/recommendation.html', context)


import pandas as pd
import math
import numpy as np
import operator

#### 추천알고리즘 ####

# 2. MovieRatings에 있는 모든 데이터를 딕셔너리 형태로 변환
def ratings_dict(mr):
    r_dict = {}
    for i in mr:
        if i.rater.pk not in r_dict.keys():
            r_dict[i.rater.pk]={i.movie.pk:float(i.score)}
        else:
            r_dict[i.rater.pk].setdefault(i.movie.pk,float(i.score))
    return r_dict

def cosine_similarity(A,B):
    A_norms = B_norms = 0
    dot_p = np.dot(A,B)
    A_norms = math.sqrt(sum([i**2 for i in A]))
    B_norms = math.sqrt(sum([i**2 for i in B]))
    AB_norms = A_norms * B_norms
    return dot_p / AB_norms # 1에 가까울수록 유사함.

# 3. KNN 기반의 사용자 기반 필터링 기법을 사용한 특정 유저에 대한 추천 영화.
def user_based_filtering(rating_dict, my, similarity=cosine_similarity, k=3):
    movies = Movie.objects.all()
    
    # db에 있는 모든 영화 데이터
    all_movie=[i.pk for i in movies]

    # (1) my(나)와 모든 사용자들이 내린 평가한 영화를 토대로 유사도를 계산한다.
    # my_rating: 내가 평점을 준 모든 영화 데이터
    my_rating = set(rating_dict[my].keys()) 
  
    similar_score={} # 사용자간 유사도 결과.
    for you in rating_dict.keys():
        if you != my:
            you_rating = set(rating_dict[you].keys())
            # (2) 나와 상대방의 교집합(intersection)를 찾는다.
            intersect = my_rating.intersection(you_rating)
            # (3) 겹치는게 최소 갯수 이상인 경우에만 유사도 측정 시작 
            if len(intersect) >= 3:
                
                # (4) 상대방과 나의 겹치는 영화의 평점을 추출해낸다
                my_rating_score = [rating_dict[my][i] for i in intersect]
                you_rating_score = [rating_dict[you][i] for i in intersect]
                # 2개의 데이터를 통해 유사도를 측정
                score= cosine_similarity(my_rating_score, you_rating_score)
    
                similar_score[you]=score
    
    # 유사도 정렬
    neighborhood=sorted(similar_score.items(), key=operator.itemgetter(1), reverse=True)

    # (5) 내가 평가하지 않은 아이템들을 추출하고, 그 아이템을 평가한 유사도 기준 이웃 k 명의 평가를 토대로 가중평균을 구함.
    # people_for_recommendation: 나와 유사도가 높은 순서대로 정렬한 user배열
    people_for_recommendation = [i[0] for i in neighborhood] 

    # no_watch_m = 모든 영화 - 내가 본영화 = 내가 못본영화
    no_watch_m = set(all_movie) - my_rating 
    recommendation_of_movies = {} 

    # (6) 내가 못본 영화(movie)를 한개씩 뽑아낸다.
    # (7) 나와 유사도가 높은 사람들중 내가 못본 영화 (movie)를 봤다면
    # (8) 해당 영화의 평점 * 나와의 유사도를 곱한값을 r 리스트에 push, s 리스트에는 유사도를 push
    # (9) 해당 영화의 추천도점수(sum(r[:k])/sum(s[:k]))를 recommendation_of_movies에 push 
    # (10) 내가 못본 모든 movie를 검사하기 위해 1~4번을 계속반복한다
    for movie in no_watch_m:
        r=[]
        s=[]
        for person in people_for_recommendation:
            if movie in rating_dict[person].keys():
                r.append(rating_dict[person][movie]*similar_score[person])
                s.append(similar_score[person])
            else:
                continue
        if (sum(r) == 0) or (sum(s)== 0): # 내가 평가하지 않은 영화에 누구도 평가 안했으면 통과
            continue
        elif len(r) <= k: 
            recommendation_of_movies[movie] = sum(r)/sum(s) 
        else:
            recommendation_of_movies[movie] = sum(r[:k])/sum(s[:k]) 
    # recommendation_of_movies을 추천도가 높은 순서대로 4개 return
    return sorted(recommendation_of_movies.items(), key=operator.itemgetter(1), reverse=True)[:4]

# 1. 추천알고리즘
def foryou(request):
    if request.user.is_authenticated:
        num = request.user.pk
        mr_cnt = MovieRatings.objects.count()
        mr = MovieRatings.objects.all()[ mr_cnt//2 : ]
        # 2. MovieRatings에 있는 모든 데이터를 딕셔너리 형태로 변환
        r_dict = ratings_dict(mr)
        if num in r_dict.keys():
            # 3. KNN 기반의 사용자 기반 필터링 기법을 사용한 특정 유저에 대한 추천 영화.
            recommend = user_based_filtering(r_dict, num)
            if len(recommend) >= 1:
                movies=  []
                for tmp in recommend:
                    movie = Movie.objects.get(pk=tmp[0])
                    movies.append(movie)
                context = {
                    "movies":movies,
                }
                return render(request,'movies/foryou.html', context)
        messages.add_message(request, messages.WARNING, '프리미엄추천을 위한 사용자의 평점데이터가 부족합니다.') 
        return redirect('movies:recommendation')
    else:
        return redirect('accounts:login')


# 영화store DB 검색 - superuser
def find_store(request):
    b = request.GET.get('b','') # GET request의 인자중에 b 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if b: # b에 값이 들어있으면 true
        movies = Moviestore.objects.filter(Q(title__contains=b) | Q(original_title__contains=b)) 
    else:
        movies = '검색어와 일치하는 결과가 없습니다.'
    context = {
        'keyword':b,
        'movies': movies,
    }
    return render(request, 'movies/findresult.html', context)

# 영화 DB추가
def plus(request, movie_pk):
    genre = {
        "Adventure":12, "Fantasy":14, "Animation":16, "Drama":18, "Horror":27, "Action":28, 
        "Comedy":35, "History":36, "Western":37, "Thriller":53, "Crime":80, "Documentary":99, 
        "Science Fiction":878, "Mystery":9648, "Music":10402, "Romance":10749, "Family":10751, "War":10752, 
        "TV Movie":10770, 
    }
    if request.user.is_authenticated:
        if request.user.is_superuser:
            moviedata = get_object_or_404(Moviestore, pk=movie_pk)
            newmovie = Movie.objects.create(
                id = moviedata.id,
                title = moviedata.title,
                original_title = moviedata.original_title,
                release_date = moviedata.release_date,
                popularity = moviedata.popularity,
                vote_count = moviedata.vote_count,
                vote_average = moviedata.vote_average,
                adult = moviedata.adult,
                overview = moviedata.overview,
                original_language = moviedata.original_language,
                poster_path = moviedata.poster_path,
                backdrop_path = moviedata.backdrop_path,
            )
            for g in moviedata.genres.all():
                print(g)
                for key,value in genre.items():
                    if value == g:
                        gen = Genre.objects.get(name=key)
                        newmovie.genres.all(gen)
                        break
                newmovie.genres.add()
            newmovie.save()
            def __str__(self):
                return self.title
            Moviestore.objects.get(pk=movie_pk).delete()
            return redirect('movies:find')
        else: 
            return redirect('movies:find')
    else:
        return redirect('accounts:login')