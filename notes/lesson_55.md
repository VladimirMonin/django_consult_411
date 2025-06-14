# Тема Django ORM Ч2. CRUD-запросы, QuerySet, связи «один-ко-многим». Урок 55

## Система моделей

```python
class Master(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(
        null=True, blank=True, max_length=100, verbose_name="Отчество"
    )
    phone = models.CharField(max_length=20, verbose_name="Телефон", default="00000000000")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        # на русском языке - в ед. числе и мн. числе
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        # сортировка по фамилии и имени
        ordering = ["last_name", "first_name"]


class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    master = models.ForeignKey(Master, verbose_name="Мастер", default=None, on_delete=models.SET_DEFAULT, related_name="orders")

```

На текущий момент система моделей осталась с прошлого занятия неизменной.
Изменилось лишь то что мы добавили `related_name="orders"` в модель `Order`.

Рассказ про `related_name`

## Shell Plus - запуск в `print sql` режиме

```bash
poetry run python manage.py shell_plus --print-sql
```

Рассказ про флаг и режим `--print-sql`

## Запросы

### Метод `Create`

```python
# Создание мастера через метод Create
master = Master.objects.create(first_name="Гендальф", last_name="Серый", phone="12345678901")
```

Видим в консоли
```txt
>>> master = Master.objects.create(first_name="Гендальф", last_name="Серый", phone="12345678901")
INSERT INTO "core_master" ("first_name", "last_name", "middle_name", "phone", "email")
VALUES ('Гендальф', 'Серый', NULL, '12345678901', NULL) RETURNING "core_master"."id"
Execution time: 0.006985s [Database: default]
```


```python
# Создание заказа через метод Create
order = Order.objects.create(name="Бильбо", phone="+12345678901", master=master, comment="Покраска бороды перед походом!")
```

### Метод `Save`

Мы можем создавать объекты, и потом их сохранять методом `save()`

```python
# Создание заказа через метод Create
order2 = Order(name="Сэм", phone="+12345678901")
# Попытка сохранить тут даст django.db.utils.IntegrityError: NOT NULL constraint failed: core_order.master_id
order2.comment = "Хоббитанский педикюр перед походом!"

# Добыть мастера
master = Master.objects.get(pk=1)
order2.master = master
# Только сейчас сохраняем заказ. Он сохранится и у объекта появится id
order2.save()
```

## Objects Manager

Объектный менеджер `objects` в Django является ключевым компонентом ORM (Object-Relational Mapper) и предоставляет интерфейс для выполнения операций с базой данных. Он автоматически добавляется к каждой модели Django и позволяет вам взаимодействовать с таблицей базы данных, связанной с этой моделью.

Вот детальная справка по `objects`:

### Что такое `objects`?

`objects` — это экземпляр класса [`django.db.models.Manager`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#manager-methods), который Django автоматически добавляет к каждой модели. Он служит точкой входа для выполнения запросов к базе данных. Через `objects` вы получаете доступ к методам, которые позволяют вам извлекать, создавать, обновлять и удалять объекты (записи) вашей модели.

### Основные методы `QuerySet`, доступные через `objects`

Когда вы вызываете методы на `objects`, они обычно возвращают [`QuerySet`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/), который представляет собой коллекцию объектов из базы данных. `QuerySet`'ы "ленивы" (lazy), что означает, что запрос к базе данных выполняется только тогда, когда вы фактически обращаетесь к данным (например, итерируете по `QuerySet` или преобразуете его в список).

Вот некоторые из наиболее часто используемых методов:

1.  **[`all()`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#all)**
    *   Возвращает новый `QuerySet`, содержащий все объекты из базы данных для данной модели.
    *   Пример: `Master.objects.all()`

2.  **[`filter(**kwargs)`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#filter)**
    *   Возвращает новый `QuerySet`, содержащий объекты, которые соответствуют заданным условиям поиска. Условия задаются как аргументы ключевых слов (field lookup).
    *   Пример: `Master.objects.filter(first_name="Гендальф")`
    *   Пример с `__icontains` (регистронезависимое вхождение): `Order.objects.filter(comment__icontains="бороды")`

3.  **[`get(**kwargs)`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#get)**
    *   Возвращает один объект, который соответствует заданным условиям поиска.
    *   Если найдено более одного объекта или ни одного объекта, будет вызвано исключение (`MultipleObjectsReturned` или `DoesNotExist` соответственно).
    *   Пример: `master = Master.objects.get(pk=1)` (как в `notes/lesson_55.md:81`)

4.  **[`exclude(**kwargs)`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#exclude)**
    *   Возвращает новый `QuerySet`, содержащий объекты, которые *не* соответствуют заданным условиям поиска.
    *   Пример: `Master.objects.exclude(last_name="Серый")`

5.  **[`order_by(*fields)`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#order-by)**
    *   Возвращает новый `QuerySet`, отсортированный по указанным полям. По умолчанию сортировка по возрастанию. Для сортировки по убыванию используйте префикс `-`.
    *   Пример: `Master.objects.all().order_by('last_name', '-first_name')`

6.  **[`create(**kwargs)`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#create)**
    *   Удобный метод для создания и сохранения нового объекта модели за одну операцию. Он создает экземпляр модели, устанавливает переданные поля и немедленно вызывает `save()`.
    *   Пример: `master = Master.objects.create(first_name="Гендальф", last_name="Серый", phone="12345678901")` (как в `notes/lesson_55.md:53`)

7.  **[`get_or_create(defaults=None, **kwargs)`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#get-or-create)**
    *   Пытается получить объект, соответствующий `kwargs`. Если объект не найден, он создает его. Возвращает кортеж `(object, created)`, где `object` — это полученный или созданный объект, а `created` — булево значение, указывающее, был ли объект создан.
    *   Пример: `master, created = Master.objects.get_or_create(first_name="Фродо", last_name="Бэггинс", defaults={'phone': '9876543210'})`

8.  **[`update(**kwargs)`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#update)**
    *   Выполняет массовое обновление для всех объектов в `QuerySet`. Возвращает количество обновленных строк.
    *   Пример: `Master.objects.filter(last_name="Серый").update(phone="00000000000")`

9.  **[`delete()`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#delete)**
    *   Выполняет массовое удаление для всех объектов в `QuerySet`. Возвращает кортеж `(количество_удаленных_объектов, словарь_по_типам_объектов)`.
    *   Пример: `Master.objects.filter(first_name="Гендальф").delete()`

10. **[`count()`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#count)**
    *   Возвращает количество объектов в `QuerySet`.
    *   Пример: `Master.objects.all().count()`

11. **[`first()`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#first)** и **[`last()`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#last)**
    *   Возвращают первый или последний объект в `QuerySet` соответственно. Возвращают `None`, если `QuerySet` пуст.
    *   Пример: `Master.objects.order_by('id').first()`

### Ленивость `QuerySet` (Lazy Evaluation)

Как упоминалось в `notes/lesson_55.md:101`, `QuerySet`'ы ленивы. Это означает, что они не выполняют запрос к базе данных немедленно при создании. Запрос выполняется только тогда, когда `QuerySet` "оценивается" (evaluated). Это происходит в следующих случаях:

*   Итерация по `QuerySet` (например, в цикле `for`).
*   Преобразование `QuerySet` в список (`list(queryset)`).
*   Использование срезов (`queryset[0:5]`).
*   Вызов методов, которые возвращают один объект (`get()`, `first()`, `last()`).
*   Вызов методов, которые агрегируют данные (`count()`, `sum()`, `avg()`).
*   Использование `repr()` или `str()` для `QuerySet` (например, при выводе в консоль `shell_plus`).

Ленивость позволяет Django оптимизировать запросы к базе данных, выполняя их только тогда, когда это действительно необходимо, и объединяя несколько операций в один запрос, если это возможно.

### Цепочечный стиль (Chain-style)

Методы `QuerySet` часто возвращают новый `QuerySet`, что позволяет "цепочечно" вызывать методы. Это очень удобно для построения сложных запросов.

Пример:
```python
# Найти всех мастеров с именем "Гендальф", отсортировать по фамилии и получить первые 5
masters = Master.objects.filter(first_name="Гендальф").order_by('last_name')[:5]
```

### `related_name` и обратные связи

В `notes/lesson_55.md:30` упоминается `related_name="orders"` в модели `Order`. Это очень важная концепция для обратных связей.

Когда у вас есть `ForeignKey` (например, `Order.master` ссылается на `Master`), Django автоматически создает "обратную" связь. Без `related_name`, вы могли бы получить все заказы для конкретного мастера через `master_instance.order_set.all()`.

Однако, используя `related_name="orders"`, вы делаете код более читаемым и интуитивно понятным:
```python
# Получить мастера с id=1
master = Master.objects.get(pk=1)

# Получить все заказы, связанные с этим мастером
# Вместо master.order_set.all() используем master.orders.all()
all_orders_for_master = master.orders.all()
```

Это делает навигацию по связям между моделями гораздо более удобной и понятной.

### Итог

Объектный менеджер `objects` — это основной инструмент для взаимодействия с базой данных в Django. Он предоставляет мощный и гибкий API для выполнения CRUD-операций и построения сложных запросов с использованием `QuerySet`'ов, которые оптимизированы благодаря ленивой оценке и цепочечному стилю вызовов. Понимание его работы является фундаментальным для эффективной разработки на Django.


## Метод `get`

Метод `get` используется для получения одного объекта из базы данных. Он принимает набор условий в виде именованных аргументов, которые соответствуют полям модели. Если объект не найден или найдено несколько объектов, будет вызвано исключение.

Идеален для добычи одного объекта по уникальному идентификатору. По `id` или если поле отмечено как `unique`.
Так как база маленькая и мастер с именем Гендальф всего один, то он будет найден.

```python
master_g = Master.objects.get(first_name="Гендальф")
```

Но если бы у нас был Гендальф Белый - мы бы получили ошибку - `MultipleObjectsReturned`.
Если бы мастеров вообще не было - мы бы получили ошибку `DoesNotExist`.

Тут стоит быть осторожным. Если мы уверены, что объект точно есть - можно использовать `get`.

## Метод `get_or_create`

Метод `get_or_create` используется для получения объекта из базы данных или создания нового, если объект не найден. Он возвращает кортеж, содержащий объект и булево значение, указывающее, был ли объект создан.

```python
master_g, created = Master.objects.get_or_create(first_name="Гендальф", last_name="Белый")
```

В первый раз мы создадим Гендальфа Белого. Во второй раз - просто получим его. Поэтому `created` будет `True` или `False`.










Цели

• Выполнять create/read/update/delete через ORM

• Понимать ленивость QuerySet

• Ходить по FK в обе стороны, использовать select_related

• Писать базовые фильтры/сортировки

Структура

00-10  Введение, связь с уроком 54

10-30  Теория 1: Manager → QuerySet, ленивость, chain-style

30-55  Практика 1: shell_plus – чтение, срезы, count, order_by

55-65  Q&A

65-85  Теория 2: CRUD-методы, get_or_create, atomic (кратко)

85-115 Практика 2: create Master/Order, update, bulk update, delete

115-130 Перерыв

130-150 Теория 3: FK «туда-обратно», related_name, select_related

150-180 Практика 3: количество заявок у мастера, мастера без заявок, профилирование

Домашнее: 10 запросов (5 чтение, 2 создание, 2 обновление, 1 удаление)

