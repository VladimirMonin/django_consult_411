# users/urls.py
from django.urls import path
from .views import register, login, logout


# Маршруты будут иметь префикс /users/
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]
