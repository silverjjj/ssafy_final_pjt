from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    # R: 리뷰 리스트를 보여주는 페이지
    path('', views.index, name='index'),
    # R: 특정 리뷰의 상세 내용을 보여주는 페이지  +  여기서 코멘트까지 처리
    path('<int:review_pk>/', views.review_detail, name="review_detail"),
    # C: 리뷰 작성(인자 = 영화pk)
    path('<int:movie_pk>/create/', views.review_create, name="review_create"),
    # U: 리뷰 수정
    path('<int:review_pk>/update/', views.review_update, name="review_update"),
    # D: 리뷰 삭제
    path('<int:review_pk>/delete/', views.review_delete, name="review_delete"),


    # 전체 리뷰 조회
    path('review_list/', views.review_list, name="review_list"),


    # -------------review좋아요----------- #
    path('<int:review_pk>/like/', views.review_like, name="review_like"),

    # -------------review 검색---------------- #
    path('find/', views.find, name="find"),
    path('find2/', views.find2, name="find2"),

    # -------------comment---------------- #
    path('<int:review_pk>/<int:comment_pk>/c_delete/', views.comment_delete, name='comment_delete'),
    # path('<int:review_pk>/<int:comment_pk>/c_update/', views.comment_update, name='comment_update'),
]
