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
- `path('', index)` означает, что функция `index` будет вызываться при обращении к корневому URL сайта (например, <http://127.0.0.1:8000/>)

### 3. Проверяем работу приложения

После создания представления и маршрута можно запустить сервер и проверить работу нашего приложения:

```bash
# Запускает сервер разработки
poetry run python manage.py runserver
```

При переходе на <http://127.0.0.1:8000/> мы увидим нашу страницу с приветствием.

Вот схема взаимодействия URLs и Views в Django:

![first_view](./images/first_view.png)

## Создание первого шаблона с переменной и рендер с передачей контекста

Использование обычного `HttpResponse` с HTML-кодом внутри функции представления не очень удобно для создания сложных страниц. Django предлагает мощную систему шаблонов, которая позволяет отделить логику представления от HTML-разметки.

### 1. Создаем папку для шаблонов

Сначала создадим папку `templates` внутри нашего приложения `core`:

```bash
mkdir core\templates
```

### 2. Создаем HTML-шаблон

Теперь создадим файл `first_template.html` в папке `templates`:

```html
<!-- filepath: c:\PY\ПРИМЕРЫ КОДА\django_consult_411\core\templates\first_template.html -->
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Барбершоп "Арбуз"</title>
</head>
<body>
    <h1>Добро пожаловать в барбершоп "{{ name }}"!</h1>
</body>
</html>
```

Здесь мы используем специальный синтаксис Django-шаблонов: `{{ name }}` — это место, где будет подставлено значение переменной `name` из контекста.

### 3. Модифицируем представление для использования шаблона

Теперь изменим функцию `index` в файле `views.py`, чтобы она использовала наш шаблон:

```python
# filepath: c:\PY\ПРИМЕРЫ КОДА\django_consult_411\core\views.py
from django.shortcuts import render
from django.http import HttpResponse

# Представление главной страницы

def index(request):
    context = {
        "name": "Арбуз"
    }
    return render(request, 'first_template.html', context)
```

В этом коде:
- Импортируем функцию `render` из `django.shortcuts`
- Создаем словарь `context` с переменной `name`
- Используем функцию `render`, которая принимает три аргумента:
  1. Объект запроса `request`
  2. Путь к шаблону `'first_template.html'`
  3. Словарь контекста `context` с переменными для шаблона

### 4. Настройка поиска шаблонов в Django

Django автоматически ищет шаблоны в папках `templates` внутри каждого приложения, указанного в `INSTALLED_APPS`. Поскольку мы уже добавили приложение `core` в `INSTALLED_APPS`, Django найдет наш шаблон.

### 5. Проверяем работу шаблона

После внесения изменений запустим сервер:

```bash
poetry run python manage.py runserver
```

При переходе на http://127.0.0.1:8000/ мы должны увидеть страницу с HTML-разметкой из нашего шаблона, где вместо `{{ name }}` будет подставлено значение "Арбуз".

### 6. Схема взаимодействия представления с шаблоном

Вот как выглядит взаимодействие между представлением и шаблоном:

![first_template](./images/first_template.png)

На схеме видно, как переменная `name` передается из контекста представления в шаблон, где используется через синтаксис `{{ name }}`.

### 7. Преимущества использования шаблонов

- **Разделение логики и представления**: код Python отделен от HTML
- **Переиспользование кода**: можно создавать базовые шаблоны и расширять их
- **Динамический контент**: легко вставлять динамические данные в HTML

