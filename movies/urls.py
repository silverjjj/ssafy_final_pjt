from django.urls import path
from . import views

app_name='movies'
urlpatterns = [
    # 메인, 상세보기, 박스오피스
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.m_detail, name="m_detail"),
    path('boxoffice/', views.boxoffice, name="boxoffice"),
    
    # 영화 검색 - 입력 & 결과
    path('find/', views.find, name="find"),
    path('find2/', views.find2, name="find2"),

    # 영화 추가
    path('<int:movie_pk>/plus/', views.plus, name="plus"),
    path('find_store/', views.find_store, name="find_store"),


    # ----------- 혜민
    path('<int:movie_pk>/rate/', views.rate, name="rate"),
    path('<int:movie_pk>/rate_update/', views.rate_update, name="rate_update"),
    path('<int:movie_pk>/rate_delete/', views.rate_delete, name="rate_delete"),

    # 영화 요청
    path('please/', views.please, name="please"),
    # 영화 좋아요
    path('<int:movie_pk>/like/', views.movie_like, name="like"),
    # 추천알고리즘
    path('foryou/', views.foryou, name="foryou"),
    # 추천 메인화면
    path('recommendation/', views.recommendation, name='recommendation'),
]