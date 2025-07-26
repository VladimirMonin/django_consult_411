# users/urls.py
from django.urls import path
from .views import register, CustomLoginView, CustomLogoutView


# Маршруты будут иметь префикс /users/
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
