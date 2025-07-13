from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from .forms import RegistrationForm, LoginForm


User = get_user_model()


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            auth_login(request, user)
            return redirect("landing")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user_cache
            if user is not None:
                auth_login(request, user)
                # Перенаправляем на next, если он есть
                return redirect(request.GET.get("next", "landing"))
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


@require_POST # Будут работать только POST-запросы!
def logout(request):
    auth_logout(request)
    return redirect("landing")
