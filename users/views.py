"""
LoginView - служебный класс для входа в систему
LogoutView - служебный класс для выхода из системы
PasswordChangeView - служебный класс для смены пароля (когда вводят и старый и новый)
PasswordResetView - служебный класс для сброса пароля (когда вводят только email) работает в паре с PasswordResetForm
PasswordResetDoneView - для уведомления об отправке инструкций по сбросу пароля
PasswordResetConfirmView - для ввода нового пароля (когда вводят новый пароль) работает в паре с SetPasswordForm
PasswordResetCompleteView - для уведомления об успешном сбросе пароля
"""

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib import messages

from django.views.generic.edit import CreateView

from django.contrib.auth.forms import (
    PasswordResetForm,
)


class CustomPasswordResetView(PasswordResetView):
    """
    Шаг 2. - Старт процесса сброса пароля - ввод email пользователя
    """

    template_name = "users/password_reset_form.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("password_reset_done")
    email_template_name = "users/password_reset_email.html"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Шаг 3. - Страничка уведомления об отправке инструкций по сбросу пароля
    """

    template_name = "users/password_reset_done.html"
    # TODO - Есть ли тут success_url?


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Шаг 5. - Ввод нового пароля"""

    template_name = "users/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Шаг 6. Сообщение об успешной смене пароля
    """

    template_name = "users/password_reset_complete.html"


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = "/"

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()
        # Message
        messages.success(
            self.request,
            f"Добро пожаловать, {user.username}! Вы успешно зарегистрировались.",
        )
        # Выполяем авторизацию
        auth_login(self.request, user)
        # Вызываем родительский метод
        return redirect("landing")

    def form_invalid(self, form):
        # Добавляем сообщение об ошибке
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "users/password_change_form.html"
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
