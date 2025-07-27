# users/urls.py
from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    RegisterView,
    CustomPasswordResetView
)


# Маршруты будут иметь префикс /users/
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path(
        "change-password/", CustomPasswordChangeView.as_view(), name="password_change_form"
    ),
    # СБРОС И ВОССТАНОВЛЕНИЕ ПАРОЛЯ
    # Шаг 2. Форма ввода емейла для сброса пароля
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset_form"),
]
