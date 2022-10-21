from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            form.save()
            auth_login(request, user)
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, "로그인 되었습니다.")
            return redirect("articles:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "로그아웃 되었습니다.")
    return redirect("articles:index")


@login_required
def profile(request, pk):
    user = User.objects.get(pk=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def userlist(request):
    users = User.objects.all()
    context = {
        "users": users,
    }
    return render(request, "accounts/userlist.html", context)


@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "회원정보 수정이 완료되었습니다.")
            return redirect("articles:index")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("articles:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    messages.success(request, "회원 탈퇴가 완료되었습니다.")
    return redirect("articles:index")
