## Создание проекта и первого Django приложения

### Мы создали новый проект Django используя poetry


```bash
# Создаст pypoetry.toml
poetry init --no-interaction
# Создаст виртуальное окружение и установит Django
poetry add django
```

Иногда Poetry не устанавливает устанавливает автоматически пакеты при команде `poetry add`, поэтому лучше использовать команду `poetry install` после добавления пакетов в `pyproject.toml`.

В нашем случае может быть ошибка, так как мы сделали пустой проект, и в нем нет пакетов. Может помочь команда: `poetry install --no-root`.

### Создание проекта Django

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


### Создание приложения core

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
    'core.apps.core',
]
```