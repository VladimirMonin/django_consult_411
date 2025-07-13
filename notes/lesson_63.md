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
