from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Count

from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from movies.models import Movie
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator

def index(request):
    if request.user.is_authenticated:
        # 모든 리뷰
        reviews = Review.objects.all()[:5]
        # 인기 리뷰
        best_reviews = Review.objects.annotate(like_count=Count('like_users')).order_by('-like_count')[:5]
        # print(best_reviews)
        # # 인기 평론가
        User = get_user_model()
        best_reviewers = User.objects.annotate(followers_count=Count('followers')).order_by('-followers_count')[:6]
        # # 내가 쓴 글
        my_reviews = request.user.review_set.order_by('-created_at')
        # # 최근 올라온 리뷰
        recent_reviews = Review.objects.order_by('-created_at')[:5]
        context = {
            'reviews':reviews,
            'best_reviews': best_reviews,
            'best_reviewers':best_reviewers,
            'recent_reviews':recent_reviews,
            'my_reviews':my_reviews,
        }
        return render(request, 'reviews/index.html', context)
    else:
        return redirect('accounts:login')

def review_list(request):
    print("1번")
    if request.user.is_authenticated:
        # 모든 리뷰
     
        reviews = Review.objects.all() 
        paginator = Paginator(reviews, 10)	# articles를 1page당 10개씩    
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)	# 페이지는 나눠주는 obj
        context = {
            'reviews':reviews,
            'page_obj':page_obj,
           }
        return render(request, 'reviews/review_list.html', context)
    else:
        return redirect('accounts:login')

def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.writer = request.user
                review.movie = get_object_or_404(Movie, pk=movie_pk)
                review.save()
                return redirect('reviews:review_detail', review.pk)
        else:
            form = ReviewForm()
        context = {
            'form':form,
            'movie':movie,
        }
        return render(request, 'reviews/forms.html', context)
    else:
        return redirect('accounts:login')

def review_update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.writer:
        if request.method == "POST":
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.writer = request.user
                review.save()
                return redirect('reviews:review_detail', review.pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'review':review,
            'form':form,
        }
        return render(request, 'reviews/forms.html', context)
    else:
        return redirect('reviews:review_detail', review.pk)

def review_detail(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.method == 'POST':
            commentform = CommentForm(request.POST)
            if commentform.is_valid():
                comment = commentform.save(commit=False)
                comment.c_writer = request.user
                comment.review = review
                comment.save()
                return redirect('reviews:review_detail', review.pk)
        else:
            commentform = CommentForm()
        context = {
            'review':review,
            'commentform':commentform
        }
        return render(request, 'reviews/review_detail.html', context)
    else:
        return redirect('accounts:login')

def review_delete(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.writer:
            review.delete()
            return redirect('reviews:index')
        else:
            return redirect('reviews:review_detail', review.pk)
    else:
        return redirect('accounts:login')

# review에 좋아요
def review_like(request, review_pk):
    if request.user.is_authenticated:
        user = request.user # 현재 로그인한 유저
        review = get_object_or_404(Review, pk=review_pk)

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user) # 좋아요 취소
            liked = False
        else:
            review.like_users.add(user) # 좋아요!
            liked = True
        data = {
            'liked':liked,
            'count':review.like_users.count(),
        }
        return JsonResponse(data)

# comment
def comment_delete(request, review_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.c_writer:
            comment.delete()
            return redirect('reviews:review_detail', review_pk)
        else:
            return redirect('reviews:review_detail', review_pk)
    else:
        return redirect('accounts:login')

def find(request):
    return render(request, 'movies/find.html')

def find2(request):
    b = request.GET.get('b','') 
    if b:
        reviews = Review.objects.filter(Q(title__icontains=b)|Q(content__icontains=b))
    else:
        reviews = '검색어와 일치하는 결과가 없습니다.'
    context = {
        'keyword':b,
        'reviews': reviews,
    }
    return render(request, 'reviews/findresult.html', context)