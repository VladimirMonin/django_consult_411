# users/urls.py
from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    RegisterView,
)


# Маршруты будут иметь префикс /users/
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path(
        "change-password/", CustomPasswordChangeView.as_view(), name="change_password"
    ),
]
