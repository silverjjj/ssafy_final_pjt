from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # /accounts/
    # path('',views.index, name='index'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.login, name = 'login'),
    path('logout/', views.logout, name="logout"),
    path('delete/', views.delete, name='delete'),
    # path('update/', views.update,name='update'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),

]