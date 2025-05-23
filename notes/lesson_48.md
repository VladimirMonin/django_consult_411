# Lesson 48: Создание проекта и первого Django приложения

## Мы создали новый проект Django используя poetry


```bash
# Создаст pypoetry.toml
poetry init --no-interaction
# Создаст виртуальное окружение и установит Django
poetry add django
```

Иногда Poetry не устанавливает устанавливает автоматически пакеты при команде `poetry add`, поэтому лучше использовать команду `poetry install` после добавления пакетов в `pyproject.toml`.

В нашем случае может быть ошибка, так как мы сделали пустой проект, и в нем нет пакетов. Может помочь команда: `poetry install --no-root`.

## Создание проекта Django

```bash
# Создает проект Django в текущей директории
poetry run django-admin startproject barbershop .
```

Мы получаем готовый проект Django.

Можно его запустить и увидеть Django Ракету!

```bash
# Запускает сервер
poetry run python manage.py runserver
```

<!-- Вставка изображдения -->
![Django Rocket](./images/django_rocket.png)


## Создание приложения core

```bash
# Создает приложение core
poetry run python manage.py startapp core
```

Проект будет выглядеть примерно так:

![start_structure](./images/start_structure.png)

## Подключение приложения core к проекту

Начнем с того, что мы создадим приложение core и подключим его к проекту. Для этого нужно добавить его в `INSTALLED_APPS` в файле `settings.py`:

```python
# barbershop/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Добавляем наше приложение (ПОСЛЕ всех встроенных приложений)
    'core',
]
```

## Создание первого маршрута и представления

После создания приложения нам нужно создать представление (view) и связать его с URL-маршрутом.

### 1. Создадим представление в файле `views.py`

Представление — это функция, которая обрабатывает HTTP-запросы и возвращает HTTP-ответы. 
Создадим простую функцию `index` в файле `core/views.py`:

```python
# filepath: c:\PY\ПРИМЕРЫ КОДА\django_consult_411\core\views.py
from django.shortcuts import render
from django.http import HttpResponse

# Представление главной страницы


def index(request):
    return HttpResponse('<h1>Приветствуем в барбершопе "Арбуз"!!!</h1>')
```

В этом коде:
- Импортируем `HttpResponse` из модуля `django.http`
- Создаем функцию `index`, которая принимает объект запроса `request`
- Возвращаем HTTP-ответ с простой HTML-строкой

### 2. Связываем представление с URL-маршрутом

Теперь нужно указать Django, какой URL-адрес должен вызывать наше представление. 
Для этого редактируем файл `barbershop/urls.py`:

```python
# filepath: c:\PY\ПРИМЕРЫ КОДА\django_consult_411\barbershop\urls.py
from django.contrib import admin
from django.urls import path
from core.views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
]
```

В этом коде:
- Импортируем нашу функцию `index` из `core.views`
- Добавляем новый маршрут в список `urlpatterns`
- `path('', index)` означает, что функция `index` будет вызываться при обращении к корневому URL сайта (например, http://127.0.0.1:8000/)

### 3. Проверяем работу приложения

После создания представления и маршрута можно запустить сервер и проверить работу нашего приложения:

```bash
# Запускает сервер разработки
poetry run python manage.py runserver
```

При переходе на http://127.0.0.1:8000/ мы увидим нашу страницу с приветствием.

Вот схема взаимодействия URLs и Views в Django:

![first_view](./images/first_view.png)

