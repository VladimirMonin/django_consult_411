# users/urls.py
from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    RegisterView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView
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
    # Шаг 3. Вью password-reset/done/ - уведомление об отправке инструкций по сбросу пароля
    path("password-reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    # Шаг 4. Пропустили. Это рендер емейл письма
    # Шаг 5. Форма ввода нового пароля важно использовать переменные <uidb64> и <token> - служебная вью будет их обрабатывать!
    path(
        "password-reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"
    ),
]
