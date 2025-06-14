# Тема Django ORM Ч2. CRUD-запросы, QuerySet, связи «один-ко-многим». Урок 55 🐍

## Система моделей 🏗️

Рассмотрим модели Master и Order, которые представляют сущности "Мастер" и "Заказ" в нашем приложении:

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
```

### Пояснения к модели Master:
- `first_name`, `last_name` - обязательные текстовые поля (CharField) с ограничением длины 100 символов
- `middle_name` - необязательное поле (может быть NULL в БД благодаря `null=True`, и не требуется при заполнении формы благодаря `blank=True`)
- `phone` - текстовое поле с дефолтным значением "00000000000"
- `email` - поле для email с валидацией формата, необязательное
- `__str__` - метод для красивого отображения объекта
- `Meta` - внутренний класс для метаданных модели:
  - `verbose_name` - человекочитаемое имя в единственном числе
  - `verbose_name_plural` - человекочитаемое имя во множественном числе
  - `ordering` - сортировка по умолчанию

```python
class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    master = models.ForeignKey(Master, verbose_name="Мастер", default=None, on_delete=models.SET_DEFAULT, related_name="orders")
```

### Пояснения к модели Order:
- `name`, `phone` - обязательные поля для данных клиента
- `comment` - необязательное текстовое поле для дополнительной информации
- `master` - связь "один-ко-многим" с моделью Master:
  - `on_delete=models.SET_DEFAULT` - при удалении мастера, заказы останутся с master_id=NULL
  - `related_name="orders"` - позволяет получать все заказы мастера через `master.orders.all()`

На текущий момент система моделей осталась с прошлого занятия неизменной.
Изменилось лишь то что мы добавили `related_name="orders"` в модель `Order`, что значительно улучшает читаемость кода при работе с обратными связями.

## Подробнее про `related_name` 🔄

Когда мы создаем связь ForeignKey (один-ко-многим), Django автоматически создает обратную связь. Без указания `related_name` доступ к связанным объектам осуществляется через `имя_модели_set` (в нашем случае было бы `order_set`).

Использование `related_name="orders"` дает нам несколько преимуществ:

1. **Улучшенная читаемость кода**:
```python
# Без related_name
master.order_set.all()  # менее интуитивно

# С related_name
master.orders.all()    # более понятно
```

2. **Более логичные названия** - мы можем выбрать осмысленное имя для связи.

3. **Избегание конфликтов** - если бы у нас было несколько связей с одной моделью, related_name помогает их различать.

Пример использования:
```python
# Получаем мастера
master = Master.objects.get(pk=1)

# Получаем все его заказы через related_name
orders = master.orders.all()  # вместо master.order_set.all()

# Можно добавлять фильтры
recent_orders = master.orders.filter(created_at__gte=timezone.now() - timedelta(days=7))
```

Важно выбирать осмысленные имена для related_name, чтобы код оставался понятным.

## Shell Plus - запуск в `print sql` режиме 🔍

Django Shell Plus с флагом `--print-sql` - мощный инструмент для изучения ORM:

```bash
poetry run python manage.py shell_plus --print-sql
```

### Что дает `--print-sql`?
1. Показывает все SQL-запросы, которые Django генерирует под капотом
2. Помогает понять, как работают QuerySet'ы
3. Позволяет анализировать производительность запросов
4. Учит писать более эффективные запросы

Пример работы:
```python
# В обычном режиме мы видим только результат
Master.objects.all()
# <QuerySet [<Master: Гендальф Серый>, <Master: Гендальф Белый>]>

# В режиме --print-sql мы видим сам запрос:
"""
SELECT "core_master"."id",
       "core_master"."first_name",
       "core_master"."last_name",
       "core_master"."middle_name",
       "core_master"."phone",
       "core_master"."email"
  FROM "core_master"
 ORDER BY "core_master"."last_name" ASC,
          "core_master"."first_name" ASC
 LIMIT 21
Execution time: 0.000149s [Database: default]
"""
```

### Советы по использованию:
1. Обращайте внимание на количество запросов (N+1 проблема)
2. Смотрите на время выполнения (Execution time)
3. Анализируйте сложность запросов (JOIN'ы, подзапросы)
4. Используйте для отладки сложных цепочек методов

Этот режим особенно полезен при:
- Оптимизации медленных запросов
- Изучении работы ORM
- Отладке сложных QuerySet'ов

## Запросы 📝

### Метод `Create` ➕

Метод `create()` позволяет создать и сохранить объект в БД одной операцией. Это самый простой способ создания новых записей.

#### Пример создания мастера:
```python
master = Master.objects.create(
    first_name="Гендальф",
    last_name="Серый",
    phone="12345678901"
)
```

Что происходит под капотом:
```txt
>>> master = Master.objects.create(first_name="Гендальф", last_name="Серый", phone="12345678901")
INSERT INTO "core_master" ("first_name", "last_name", "middle_name", "phone", "email")
VALUES ('Гендальф', 'Серый', NULL, '12345678901', NULL) RETURNING "core_master"."id"
Execution time: 0.006985s [Database: default]
```

#### Ключевые особенности:
1. Создает и сохраняет объект в одном методе
2. Возвращает созданный объект
3. Для обязательных полей нужно передавать значения
4. Для необязательных полей можно не передавать значения (будут NULL или default)

#### Пример создания заказа с связью:
```python
order = Order.objects.create(
    name="Бильбо",
    phone="+12345678901",
    master=master,  # передаем объект мастера
    comment="Покраска бороды перед походом!"
)
```

#### Когда использовать create():
- Когда нужно просто создать объект со всеми данными
- Когда не требуется дополнительная обработка перед сохранением
- В тестах и seed-скриптах для быстрого наполнения БД

#### Альтернатива - создание через конструктор + save():
```python
master = Master(first_name="Гендальф", last_name="Серый")
master.save()  # явное сохранение
```

### Метод `Save` 💾

Метод `save()` используется для сохранения изменений в объекте. В отличие от `create()`, он работает с уже существующими или новыми объектами.

#### Основные сценарии использования:
1. Создание нового объекта (альтернатива create())
2. Обновление существующего объекта
3. Частичное сохранение изменений

#### Пример создания заказа:
```python
# Создаем объект без сохранения в БД
order2 = Order(name="Сэм", phone="+12345678901")
order2.comment = "Хоббитанский педикюр перед походом!"

# Попытка сохранить сейчас вызовет ошибку:
# django.db.utils.IntegrityError: NOT NULL constraint failed: core_order.master_id
# потому что master - обязательное поле

# Получаем мастера
master = Master.objects.get(pk=1)
order2.master = master

# Сохраняем заказ
order2.save()  # теперь объект сохранится и получит id
```

#### Что происходит при save():
1. Для нового объекта:
   - Выполняется INSERT запрос
   - Объекту присваивается id
2. Для существующего объекта:
   - Выполняется UPDATE запрос
   - Обновляются только измененные поля

#### Когда использовать save() вместо create():
- Когда нужно создать объект поэтапно
- Когда требуется дополнительная обработка перед сохранением
- Для обновления существующих объектов
- Для частичного сохранения (например, только одного поля)

#### Пример обновления:
```python
order = Order.objects.get(pk=1)
order.comment = "Обновленный комментарий"
order.save()  # обновит только поле comment
```

#### Важные нюансы:
1. `save()` вызывает сигналы модели (pre_save, post_save)
2. Можно передать `update_fields` для оптимизации:
   ```python
   order.save(update_fields=['comment'])
   ```
3. Для массового обновления лучше использовать `update()`

## Objects Manager 🛠️

Объектный менеджер `objects` в Django является ключевым компонентом ORM (Object-Relational Mapper) и предоставляет интерфейс для выполнения операций с базой данных. Он автоматически добавляется к каждой модели Django и позволяет вам взаимодействовать с таблицей базы данных, связанной с этой моделью.

Вот детальная справка по `objects`:

### Что такое `objects`? 🤔

`objects` — это экземпляр класса [`django.db.models.Manager`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#manager-methods), который Django автоматически добавляет к каждой модели. Он служит точкой входа для выполнения запросов к базе данных. Через `objects` вы получаете доступ к методам, которые позволяют вам извлекать, создавать, обновлять и удалять объекты (записи) вашей модели.

### Основные методы `QuerySet`, доступные через `objects` 📋

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

### Ленивость `QuerySet` (Lazy Evaluation) ⏳

Как упоминалось в `notes/lesson_55.md:101`, `QuerySet`'ы ленивы. Это означает, что они не выполняют запрос к базе данных немедленно при создании. Запрос выполняется только тогда, когда `QuerySet` "оценивается" (evaluated). Это происходит в следующих случаях:

*   Итерация по `QuerySet` (например, в цикле `for`).
*   Преобразование `QuerySet` в список (`list(queryset)`).
*   Использование срезов (`queryset[0:5]`).
*   Вызов методов, которые возвращают один объект (`get()`, `first()`, `last()`).
*   Вызов методов, которые агрегируют данные (`count()`, `sum()`, `avg()`).
*   Использование `repr()` или `str()` для `QuerySet` (например, при выводе в консоль `shell_plus`).

Ленивость позволяет Django оптимизировать запросы к базе данных, выполняя их только тогда, когда это действительно необходимо, и объединяя несколько операций в один запрос, если это возможно.

### Цепочечный стиль (Chain-style) ⛓️

Методы `QuerySet` часто возвращают новый `QuerySet`, что позволяет "цепочечно" вызывать методы. Это очень удобно для построения сложных запросов.

Пример:
```python
# Найти всех мастеров с именем "Гендальф", отсортировать по фамилии и получить первые 5
masters = Master.objects.filter(first_name="Гендальф").order_by('last_name')[:5]
```

### `related_name` и обратные связи 🔄

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

### Итог 🎯

Объектный менеджер `objects` — это основной инструмент для взаимодействия с базой данных в Django. Он предоставляет мощный и гибкий API для выполнения CRUD-операций и построения сложных запросов с использованием `QuerySet`'ов, которые оптимизированы благодаря ленивой оценке и цепочечному стилю вызовов. Понимание его работы является фундаментальным для эффективной разработки на Django.


## Метод `Get` 🔍

Метод `get()` используется для получения одного объекта из базы данных по заданным критериям. Это основной метод для получения конкретной записи, когда вы ожидаете только один результат.

### Ключевые особенности:
1. Возвращает один объект, соответствующий условиям
2. Если объект не найден - вызывает исключение `DoesNotExist`
3. Если найдено несколько объектов - вызывает исключение `MultipleObjectsReturned`
4. Идеально подходит для поиска по первичному ключу (pk/id) или уникальным полям

### Примеры использования:

```python
# Получение по первичному ключу (самый надежный способ)
master = Master.objects.get(pk=1)
order = Order.objects.get(pk=1)

# Получение по уникальному полю
master = Master.objects.get(first_name="Гендальф")

# Комбинированные условия
master = Master.objects.get(first_name="Гендальф", last_name="Серый")
```

### Обработка исключений:

Всегда обрабатывайте возможные исключения при использовании get():

```python
try:
    master = Master.objects.get(first_name="Гендальф")
except Master.DoesNotExist:
    print("Мастер не найден")
except Master.MultipleObjectsReturned:
    print("Найдено несколько мастеров")
```

### Когда использовать get():
- Когда вам нужен один конкретный объект
- Когда вы ищете по первичному ключу или уникальному полю
- Когда вы уверены, что условию соответствует только один объект

### Альтернативы:
- `filter().first()` - когда возможны несколько результатов
- `get_or_create()` - когда нужно создать объект, если он не существует

## Метод `get_or_create` 🔄

Метод `get_or_create` используется для получения объекта из базы данных или создания нового, если объект не найден. Он возвращает кортеж, содержащий объект и булево значение, указывающее, был ли объект создан.

```python
master_g, created = Master.objects.get_or_create(first_name="Гендальф", last_name="Белый")
```

В первый раз мы создадим Гендальфа Белого. Во второй раз - просто получим его. Поэтому `created` будет `True` или `False`.


## Метод `Filter` 🎯

Метод `filter()` - основной инструмент для выборки данных в Django ORM. Он возвращает QuerySet объектов, соответствующих заданным критериям.

### Ключевые особенности:
1. Возвращает QuerySet (может содержать 0, 1 или много объектов)
2. Поддерживает цепочечный вызов методов
3. Ленивая оценка - запрос выполняется только при необходимости
4. Позволяет строить сложные условия выборки

### Примеры использования:

#### Базовые фильтры:
```python
# Простое равенство
masters = Master.objects.filter(first_name="Гендальф")

# Несколько условий (AND)
masters = Master.objects.filter(
    first_name="Гендальф",
    last_name="Серый"
)

# Исключение (NOT)
masters = Master.objects.exclude(last_name="Белый")

# Сравнения
orders = Order.objects.filter(created_at__gte=timezone.now() - timedelta(days=7))
```

#### Фильтрация по связанным объектам:
```python
# Получить заказы конкретного мастера
orders = Order.objects.filter(master=master)

# Получить мастеров, у которых есть заказы
masters = Master.objects.filter(orders__isnull=False)

# Фильтр по полям связанной модели
orders = Order.objects.filter(master__first_name="Гендальф")
```

#### Специальные фильтры:
```python
# Содержит подстроку (регистрозависимо)
orders = Order.objects.filter(comment__contains="бород")

# Содержит подстроку (регистронезависимо)
orders = Order.objects.filter(comment__icontains="бород")

# Вхождение в список
masters = Master.objects.filter(first_name__in=["Гендальф", "Саруман"])

# Диапазон дат
from datetime import datetime, timedelta
week_ago = datetime.now() - timedelta(days=7)
orders = Order.objects.filter(created_at__range=(week_ago, datetime.now()))
```

### Оптимизация запросов:
1. `select_related()` - для ForeignKey (один-ко-многим)
```python
orders = Order.objects.select_related('master').all()
```

2. `prefetch_related()` - для ManyToMany и обратных связей
```python
masters = Master.objects.prefetch_related('orders').all()
```

3. `only()`/`defer()` - выбор только нужных полей
```python
masters = Master.objects.only('first_name', 'last_name')
```

### Цепочки методов:
```python
# Пример сложной цепочки
recent_orders = (Order.objects
                 .filter(master=master)
                 .exclude(status='canceled')
                 .order_by('-created_at')
                 .select_related('master')
                 [:10])
```

### Когда использовать filter():
- Когда нужно получить несколько объектов
- Для построения сложных условий выборки
- Для поиска по частичным совпадениям
- Для работы с диапазонами значений

## QuerySet - что это и как он работает? 🧠

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

## Практика c ORM 🏋️

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

## Работа со связанными данными 🤝

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

## Обновление данных через `Update` и `Save` 🔄

### Создадим новую заявку 📝

```python
new_order = Order(name="Горлум", phone="1234567890", comment="Новая заявка", master=first_master)
new_order.save()
```

### Обновим заявку через `save` 💾

```python
new_order.name = "Смиргол"
new_order.save()
```


### Обновим заявку через `update` 🔄
```python
# new_order.update(name="Горлум", comment="Мне нужна услуга полировки золотого кольца!")
Order.objects.filter(name="Смиргол").update(name="Горлум", comment="Мне нужна услуга полировки золотого кольца!")

```

## Удаление данных через `delete` 🗑️

Метод `delete()` используется для удаления объектов из базы данных. Он может быть вызван как для отдельного объекта, так и для всего QuerySet.

### Основные способы удаления:

1. **Удаление одного объекта**:
```python
order = Order.objects.get(pk=1)
order.delete()  # удаляем конкретный объект
```

2. **Массовое удаление через QuerySet**:
```python
# Удаляем все заказы Горлума
Order.objects.filter(name="Горлум").delete()
```

### Что происходит при delete():

1. Вызываются сигналы `pre_delete` и `post_delete`
2. Удаляются связанные объекты в зависимости от `on_delete` в ForeignKey
3. Возвращается кортеж `(количество_удаленных_объектов, словарь_по_типам_объектов)`

### Пример с возвращаемым значением:
```python
deleted = Order.objects.filter(priority__lt=3).delete()
print(deleted)
# (5, {'core.Order': 5}) - удалено 5 объектов Order
```

### Особенности и рекомендации:

1. **Безопасность**: Всегда проверяйте QuerySet перед удалением:
```python
orders = Order.objects.filter(name="Горлум")
if orders.exists():  # проверка наличия объектов
    orders.delete()
```

2. **Каскадное удаление**: Учитывайте параметры `on_delete` в связях:
- `CASCADE` (по умолчанию) - удалит связанные объекты
- `PROTECT` - запретит удаление, если есть связанные объекты
- `SET_NULL` - установит NULL в связях
- `SET_DEFAULT` - установит значение по умолчанию

3. **Альтернативы**:
- `queryset.update(is_active=False)` - "мягкое" удаление
- Переопределение `delete()` в модели для кастомной логики

4. **Производительность**: Для массового удаления используйте QuerySet.delete() вместо цикла:
```python
# Плохо (N+1 запросов):
for order in Order.objects.filter(...):
    order.delete()

# Хорошо (1 запрос):
Order.objects.filter(...).delete()
```

### Пример безопасного удаления:
```python
try:
    # Удаляем только если есть ровно один подходящий заказ
    order = Order.objects.get(name="Горлум", phone="1234567890")
    order.delete()
except Order.DoesNotExist:
    print("Заказ не найден")
except Order.MultipleObjectsReturned:
    print("Найдено несколько заказов - нужен более точный фильтр")
```