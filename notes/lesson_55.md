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


## Filter - метод для фильтрации данных

Метод `filter` используется для получения всех объектов, которые соответствуют заданным условиям. Он возвращает `QuerySet`, который можно продолжать фильтровать или сортировать.

```python
# Получаем "обещание" получить всех мастеров с именем Гендальф.
masters_g = Master.objects.filter(first_name="Гендальф")
masters_g # Тут выполнится запрос. Мы получим QuerySet 2 мастерами
# <QuerySet [<Master: Гендальф Белый>, <Master: Гендальф Серый>]>
```

Основная фишка этого - ленивость ORM. Мы можем продложать накидывать условия выборки на переменную `masters_g`. до тех пор, пока не вызовем её.

Очень полезно для поисковых форм, чекбоксов и т.д.
```python
masters_g = Master.objects.filter(first_name="Гендальф")
masters_g = masters_g.filter(last_name="Серый")
masters_g # Тут выполнится запрос. Мы получим QuerySet с 1 мастером
```

Запрос не будет выполнен, пока мы не вызовем `masters_g`.

```txt
>>> masters_g = masters_g.filter(last_name="Серый")
>>> masters_g = masters_g.filter(last_name="Серый")
>>> masters_g
SELECT "core_master"."id",
       "core_master"."first_name",
       "core_master"."last_name",
       "core_master"."middle_name",
       "core_master"."phone",
       "core_master"."email"
  FROM "core_master"
 WHERE ("core_master"."first_name" = 'Гендальф' AND "core_master"."last_name" = 'Серый')
 ORDER BY "core_master"."last_name" ASC,
          "core_master"."first_name" ASC
 LIMIT 21
Execution time: 0.000149s [Database: default]
<QuerySet [<Master: Гендальф Серый>]>
```

## QuerySet - что это и как он работает?

Теория по `QuerySet` в Django:

### Что такое `QuerySet`?

`QuerySet` в Django — это коллекция объектов из вашей базы данных. Технически это итератор.

Это не просто список объектов, а мощный объект, который представляет собой набор записей, которые могут быть извлечены из базы данных. Думайте о `QuerySet` как о "строителе запросов" к базе данных. Когда вы создаете `QuerySet`, Django еще не обращается к базе данных; он просто строит внутреннее представление SQL-запроса.

Например, когда вы пишете `Master.objects.all()`, вы получаете `QuerySet`, который представляет "всех мастеров". Когда вы добавляете `filter()`, например `Master.objects.filter(first_name="Гендальф")`, вы уточняете этот `QuerySet`, чтобы он представлял "всех мастеров с именем Гендальф".

### Зачем нужен `QuerySet`?

`QuerySet` нужен по нескольким ключевым причинам:

1.  **Абстракция от SQL:** Он позволяет вам взаимодействовать с базой данных, используя Python-код, а не писать сырые SQL-запросы. Это делает код более читаемым, поддерживаемым и менее подверженным ошибкам, связанным с синтаксисом SQL или различиями между базами данных.
2.  **Ленивая оценка (Lazy Evaluation):** Это одна из самых важных особенностей `QuerySet`. Как упоминалось ранее, `QuerySet` не выполняет запрос к базе данных немедленно. Запрос отправляется в базу данных только тогда, когда данные действительно нужны (например, когда вы начинаете итерировать по `QuerySet`, обращаетесь к его элементам по индексу, или вызываете методы, которые требуют немедленного получения данных, такие как `list()`, `count()`, `get()`). Это значительно повышает производительность, так как Django может оптимизировать запросы, объединяя несколько операций в один SQL-запрос.
3.  **Цепочечный стиль (Chaining):** Методы `QuerySet` возвращают новый `QuerySet`, что позволяет вам "цепочечно" вызывать несколько методов для построения сложных запросов. Это делает код очень выразительным и компактным. Например, `Master.objects.filter(...).order_by(...).count()`.
4.  **Кэширование:** После того как `QuerySet` был оценен (то есть, запрос к базе данных был выполнен и данные получены), результаты кэшируются. Это означает, что если вы снова обратитесь к тому же `QuerySet`, Django не будет выполнять запрос к базе данных повторно, а вернет данные из кэша, что еще больше улучшает производительность.

### Что позволяет делать `QuerySet`?

`QuerySet` предоставляет широкий набор методов для выполнения различных операций с данными:

1.  **Выборка данных:**
    *   `all()`: Получить все объекты модели.
    *   `filter()`: Выбрать объекты, соответствующие определенным условиям.
    *   `exclude()`: Выбрать объекты, *не* соответствующие определенным условиям.
    *   `get()`: Получить один конкретный объект (вызывает ошибку, если найдено 0 или >1 объектов).
    *   `first()`, `last()`: Получить первый или последний объект в отсортированном `QuerySet`.

2.  **Сортировка данных:**
    *   `order_by()`: Отсортировать результаты по одному или нескольким полям.

3.  **Ограничение результатов (срез):**
    *   Использование срезов Python (например, `[0:10]`) для ограничения количества возвращаемых объектов, что соответствует SQL-операторам `LIMIT` и `OFFSET`.

4.  **Создание, обновление и удаление данных:**
    *   `create()`: Создать и сохранить новый объект в базе данных.
    *   `update()`: Массово обновить поля для всех объектов в `QuerySet`.
    *   `delete()`: Массово удалить объекты из базы данных.

5.  **Подсчет:**
    *   `count()`: Получить количество объектов в `QuerySet`.

Таким образом, `QuerySet` является центральным элементом Django ORM, предоставляя гибкий, эффективный и интуитивно понятный способ взаимодействия с базой данных.

## Практика c ORM

```python
# Получить ВСЕХ мастеров
masters = Master.objects.all()
[master.first_name for master in masters]

# Первый из коллекции
# first_master = Master.objects.first()
first_master = masters[0]

# Проверка на существование .exists()
Master.objects.filter(first_name='Саурон').exists()
>>> False
```

## Работа со связанными данными

В Django ORM это происходит очень естественно. Мы просто обращаемся к полю, которое является ForeignKey.

```python
# Получить все заказы
orders = Order.objects.all()

# Получить последний заказ
last_order = orders.last()

# Получить его мастера
last_order.master
```

В обратную сторону это работает так же просто. Мы обращаемся к полю, которое является `related_name` в модели `Master`.

```python
all_masters = Master.objects.all()
all_masters.count() # 3
# Берем первого

first_master = all_masters.first()
first_master.orders
# <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x0000025476295A90>
first_master.orders.all()

# А как бы оно было, если бы мы не дали related_name в Order
first_masters_orders = Order.objects.filter(master=first_master).all()
first_masters_orders = Order.objects.filter(master__id=1).all()
```

## Обновление данных через `Update` и `Save`

### Создадим новую заявку

```python
new_order = Order(name="Горлум", phone="1234567890", comment="Новая заявка", master=first_master)
new_order.save()
```

### Обновим заявку через `save`

```python
new_order.name = "Смиргол"
new_order.save()
```


### Обновим заявку через `update`
```python
# new_order.update(name="Горлум", comment="Мне нужна услуга полировки золотого кольца!")
Order.objects.filter(name="Смиргол").update(name="Горлум", comment="Мне нужна услуга полировки золотого кольца!")

```

## Удаление данных через `delete`

Удалим заявку от Горлума

```python
Order.objects.filter(name="Горлум").delete()
```
Обратите внимание, тут мы удаляем ВЕСЬ кверисет, а не один объект. Все заявки от всех Горлумов будут удалены.