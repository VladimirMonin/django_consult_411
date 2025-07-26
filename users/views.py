from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
)
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.contrib import messages


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


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "users/change_password.html"
    form_class = CustomPasswordChangeForm
    success_url = "/"


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        """Вызывается при успешной аутентификации."""
        # Получаем залогиненного пользователя
        user = form.get_user()
        # Добавляем сообщение об успехе
        messages.success(self.request, f"Добро пожаловать, {user.username}!")
        # Вызываем родительский метод, который выполняет вход и редирект
        return super().form_valid(form)

    def form_invalid(self, form):
        """Вызывается, если форма невалидна (ошибка входа)."""
        # Добавляем сообщение об ошибке
        messages.error(self.request, "Неверное имя пользователя или пароль.")
        # Вызываем родительский метод, который снова рендерит страницу с формой
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = "landing"
