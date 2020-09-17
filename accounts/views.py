from django.shortcuts import render, redirect,get_object_or_404
from .forms import CustomUserCreationForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request, user)   # 회원가입 하자마자 바로 로그인
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form,
    }
    return render(request,'accounts/form.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request,'accounts/form.html',context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

# 계정삭제
@require_POST
def delete(request):
    if request.user.is_superuser:
        request.user.delete()
    
    return redirect('movies:index')


def follow(request, user_pk):
    if request.user.is_authenticated:
        User = get_user_model()
        user = get_object_or_404(User, pk=user_pk)
        if request.user != user:
            if request.user in user.followers.all():
                user.followers.remove(request.user)
                followed = False
            else:
                user.followers.add(request.user)
                followed = True
            data = {
                'followed':followed,
                'followercount':user.followers.count()
            }
            return JsonResponse(data)