# Lesson 54


## Миграции Django
Традиционно нас встречает сообщение про 18 служебных не примененных миграций.

### Что такое миграции?

### Команды `makemigrations` и `migrate`

poetry run python manage.py makemigrations
poetry run python manage.py migrate

### Что происходит в Базе данных?



## Первая модель Django ORM

from django.db import models

class Master(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    middle_name = models.CharField()


### Применение миграций


Мы создаем миграцию `poetry run python manage.py makemigrations` и применяем ее `poetry run python manage.py migrate`.

В базе данных видим таблицу `core_master`.

`core` - название приложения, `master` - название модели.

![первая модель](./images/first_model.png)


Коммит: lesson_54: первая модель


It is impossible to add a non-nullable field 'phone' to master without specifying a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
Select an option: 


## Изменение модели

И мы понимаем что забыли добавить поле `phone`.

class Master(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    middle_name = models.CharField()
    phone = models.CharField()

Однако при попытке сделать файл миграций командой `poetry run python manage.py makemigrations` мы получаем сообщение.

It is impossible to add a non-nullable field 'phone' to master without specifying a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
Select an option: 

Мы можем выбрать второй вариант и модифицировать модель.

phone = models.CharField(null=True, default=None)

Таким образом Django Миграции заботятся о том чтобы не потерять данные. Потому что не совсем понятно, что вписать в новое поле для существующих записей.

Мы делаем миграции и применяем их.

## Откатить миграции

Мы можем откатить миграции приложения.

`poetry run python manage.py migrate core 0001`

Или же вообще вернуться в начальное состояние.
`poetry run python manage.py migrate core zero`



## Создание суперпользователя
poetry run python manage.py createsuperuser