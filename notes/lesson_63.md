# Тема Django Auth Ч1. Авторизация и логаут на функциях. Урок 63

## Создание и подключение  приложения users

`poetry run python manage.py startapp users`

Подключим его в `settings.py`

```python
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "core",
    "users", # NEW)
]
```

## Создаем собственный `urls.py` для я приложения users

```python
# users/urls.py
from django.urls import path
from .views import register, login, logout


# Маршруты будут иметь префикс /users/
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]
```

Подключаем его в `urls.py` в `barbershop` конфигурационном пакете

```python
# barbershop/urls.py
from users import urls as users_urls
urlpatterns = [
    ...
    # Пользователи
    path("users/", include(users_urls))
]
```

Теперь все адреса приложения users будут иметь префикс `/users/`

## Создаем вью - заглушки

```python
from django.shortcuts import render, HttpResponse


def register(request):
    return HttpResponse("Регистрация")


def login(request):
    return HttpResponse("Авторизация")


def logout(request):
    return HttpResponse("Выход")
```

# Минимальный вариант login - logout - register

```python
# users/forms.py
from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Неверное имя пользователя или пароль.")
            # Сохраняем пользователя в форме для последующего использования во вью
            self.user_cache = user
        return cleaned_data
```

Шаблоны
```html
{% extends 'base.html' %}

{% block title %}Вход{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title text-center">Вход</h2>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                            <div class="alert alert-danger">
                                {{ form.non_field_errors }}
                            </div>
                        {% endif %}

                        {% for field in form %}
                            <div class="mb-3">
                                <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                                {{ field }}
                                {% if field.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ field.errors.as_text }}
                                    </div>
                                {% endif %}
                            </div>
                        {% endfor %}
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-dark">Войти</button>
                        </div>
                    </form>
                </div>
                <div class="card-footer text-center">
                    <small>Нет аккаунта? <a href="{% url 'register' %}">Зарегистрироваться</a></small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

```html
{% extends 'base.html' %}

{% block title %}Регистрация{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title text-center">Регистрация</h2>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                            <div class="alert alert-danger">
                                {{ form.non_field_errors }}
                            </div>
                        {% endif %}

                        {% for field in form %}
                            <div class="mb-3">
                                <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                                {{ field }}
                                {% if field.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ field.errors.as_text }}
                                    </div>
                                {% endif %}
                            </div>
                        {% endfor %}
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-dark">Зарегистрироваться</button>
                        </div>
                    </form>
                </div>
                <div class="card-footer text-center">
                    <small>Уже есть аккаунт? <a href="{% url 'login' %}">Войти</a></small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Вьюшки

```python
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
```

Меню инклюд
```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">Барбершоп</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Переключатель навигации">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        {% for menu_item in menu %}
          <li class="nav-item">
            <a class="nav-link" href="{{ menu_item.url }}">{{ menu_item.name }}</a>
          </li>
        {% endfor %}
      </ul>
      <ul class="navbar-nav ms-auto">
        {% if user.is_authenticated %}
          <li class="nav-item">
            <span class="nav-link">Привет, {{ user.username }}!</span>
          </li>
          <li class="nav-item">
            <form action="{% url 'logout' %}" method="post" class="d-inline">
              {% csrf_token %}
              <button type="submit" class="nav-link btn btn-link">Выход</button>
            </form>
          </li>
        {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'login' %}">Войти</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'register' %}">Зарегистрироваться</a>
          </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
```

# Вариант с специализированными формами