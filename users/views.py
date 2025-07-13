from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("landing")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(request.GET.get("next", "landing"))
    else:
        form = CustomAuthenticationForm()
    return render(request, "users/login.html", {"form": form})


@require_POST
def logout(request):
    auth_logout(request)
    return redirect("landing")
