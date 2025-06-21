<!-- 
МОДЕЛИ
from django.db import models

class Master(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(
        null=True, blank=True, max_length=100, verbose_name="Отчество"
    )
    phone = models.CharField(
        max_length=20, verbose_name="Телефон", default="00000000000"
    )
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="masters")

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
    master = models.ForeignKey(
        Master,
        verbose_name="Мастер",
        default=None,
        on_delete=models.SET_DEFAULT,
        related_name="orders",
    )
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="orders")

class Review(models.Model):

    RATING_CHOICES = [
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    ]

    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Имя клиента"
    )
    master = models.ForeignKey(
        Master, on_delete=models.SET_NULL, null=True, verbose_name="Мастер"
    )
    photo = models.ImageField(
        upload_to="reviews/", blank=True, null=True, verbose_name="Фотография"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка", choices=RATING_CHOICES, default=5
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(
        verbose_name="Длительность", help_text="Время выполнения в минутах", default=20
    )
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")

    def __str__(self):
        return self.name

 -->

# Тема Django ORM Ч4. LookUp и знакомство с Q. Урок 57

## Что такое LookUp? 🔍

Лукапы (LookUp) — это способ фильтрации данных в Django ORM. Они позволяют выполнять сложные запросы к базе данных, используя условные выражения и операторы.

Выглядят они примерно так:

```python
from django.db.models import Q

```python
# Фильтрация Заявок по имени мастера
orders = Order.objects.filter(master__first_name="Алевтина")
```

`__` - Это и есть лукап.
`master__first_name` - запрос на фильтрацию по полю `first_name` модели `Master`.

### Примеры простых лукапов

Запускаем shell plus в режиме print_sql
`poetry run python manage.py shell_plus --print-sql`

Без лукапа мы могли бы начать с обратной стороны и взять мастера по имени, и вытянуть все заявки, которые он принял.

```python
# Фильтрация Заявок по имени мастера
master = Master.objects.get(first_name="Алевтина")
orders = Order.objects.filter(master=master)

# Или даже в одну строку
aleftina_orders = Master.objects.get(first_name="Алевтина").orders.all()
```

### Таблица лукапов для условий выборки.

| Lookup      | Описание                                                                                                                                     | Пример использования                                             |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| exact       | Возвращает объекты, у которых значение указанного поля точно совпадает с заданным значением.                                                 | Master.objects.filter(first_name__exact='Алевтина')              |
| iexact      | Возвращает объекты, у которых значение указанного поля точно совпадает с заданным значением без учета регистра.                              | Master.objects.filter(first_name__iexact='алевтина')             |
| contains    | Возвращает объекты, у которых значение указанного поля содержит заданную подстроку.                                                          | Service.objects.filter(name__contains='стрижка')                 |
| icontains   | Возвращает объекты, у которых значение указанного поля содержит заданную подстроку без учета регистра.                                       | Service.objects.filter(name__icontains='СТРИЖКА')                |
| in          | Возвращает объекты, у которых значение указанного поля находится в списке заданных значений.                                                 | Master.objects.filter(id__in=[1, 2, 3])                         |
| gt          | Возвращает объекты, у которых значение указанного поля больше заданного значения.                                                            | Service.objects.filter(price__gt=1000)                          |
| gte         | Возвращает объекты, у которых значение указанного поля больше или равно заданному значению.                                                  | Service.objects.filter(price__gte=1000)                         |
| lt          | Возвращает объекты, у которых значение указанного поля меньше заданного значения.                                                            | Service.objects.filter(price__lt=1000)                          |
| lte         | Возвращает объекты, у которых значение указанного поля меньше или равно заданному значению.                                                  | Service.objects.filter(price__lte=1000)                         |
| startswith  | Возвращает объекты, у которых значение указанного поля начинается с заданной подстроки.                                                      | Master.objects.filter(last_name__startswith='Ив')                |
| istartswith | Возвращает объекты, у которых значение указанного поля начинается с заданной подстроки без учета регистра.                                   | Master.objects.filter(last_name__istartswith='ив')               |
| endswith    | Возвращает объекты, у которых значение указанного поля заканчивается на заданную подстроку.                                                  | Master.objects.filter(last_name__endswith='ов')                  |
| iendswith   | Возвращает объекты, у которых значение указанного поля заканчивается на заданную подстроку без учета регистра.                               | Master.objects.filter(last_name__iendswith='ОВ')                 |
| range       | Возвращает объекты, у которых значение указанного поля находится в заданном диапазоне.                                                       | Service.objects.filter(price__range=(500, 2000))                 |
| date        | Возвращает объекты, у которых значение указанного поля является датой, равной заданной дате.                                                 | Review.objects.filter(created_at__date=datetime.date(2025, 6, 1))|
| year        | Возвращает объекты, у которых значение указанного поля является годом, равным заданному году.                                                | Review.objects.filter(created_at__year=2025)                     |
| month       | Возвращает объекты, у которых значение указанного поля является месяцем, равным заданному месяцу.                                            | Review.objects.filter(created_at__month=6)                       |
| day         | Возвращает объекты, у которых значение указанного поля является днем, равным заданному дню.                                                  | Review.objects.filter(created_at__day=1)                         |
| week_day    | Возвращает объекты, у которых значение указанного поля является днем недели, равным заданному дню недели. (0 - понедельник, 6 - воскресенье) | Review.objects.filter(created_at__week_day=0)                    |
| isnull      | Возвращает объекты, у которых значение указанного поля является NULL или не NULL.                                                            | Master.objects.filter(middle_name__isnull=True)                  |
| regex       | Возвращает объекты, у которых значение указанного поля соответствует заданному регулярному выражению.                                        | Master.objects.filter(first_name__regex=r'^[А-Яа-я]+$')          |

## Практика с фильтрацией через лукапы

Лукап - не всегда история про Join таблиц, как это было в первом примере. Это часто так же и работа в одной таблице где нам надо использовать логические операторы SQL.

Такие операторы как `IN`, `BETWEEN`, `LIKE` и т.д.

### Услуга где название содержит стрижка
```python
query1 = Service.objects.filter(name__contains='бород')
```

Тут использован `__contains` - это оператор, который проверяет, содержит ли значение поля указанную подстроку.

SLQ запрос будет формата `WHERE "core_service"."name" LIKE '%стрижка%'`

### Мастера по списку id

```python
query2 = Master.objects.filter(id__in=[1, 2, 3])
```

Лукап `__in` - это оператор, который проверяет вхождение в список значений.

SQL запрос будет формата `WHERE "core_master"."id" IN (1, 2, 3)`

### Услуги с ценой больше или равной 1000
```python
Service.objects.filter(price__gte=1000)
```

Тут использован `__gte` - это оператор, который проверяет, больше или равно значение поля указанному значению.

SQL запрос будет формата `WHERE "core_service"."price" >= '1000'`

### Услуги с ценой между 500 и 2000
```python
Service.objects.filter(price__range=(500, 2000))
```

Тут использован `__range` - это оператор, который проверяет, находится ли значение поля в заданном диапазоне.

SQL запрос будет формата `WHERE "core_service"."price" BETWEEN '500' AND '2000'`

### Мастера, которые заканчиваются на "ый"
```python
Master.objects.filter(last_name__endswith='ый')
```
Тут использован `__endswith` - это оператор, который проверяет, заканчивается ли значение поля на указанную подстроку.

### Услуги, которые были созданы в 2025 году

```python
Review.objects.filter(created_at__year=2025)
```

Тут использован `__year` - это оператор, который проверяет, является ли значение поля годом, равным заданному году.

SQL запрос формата:
`WHERE "core_review"."created_at" BETWEEN '2025-01-01 00:00:00' AND '2025-12-31 23:59:59.999999'`

### Записи на услугу позже 2024 года
```python
import datetime
Review.objects.filter(created_at__gt=datetime.date(2025, 1, 1))

# Или через __year
Review.objects.filter(created_at__year__gt=2024)
```

WHERE "core_review"."created_at" > '2025-01-01 00:00:00'
WHERE "core_review"."created_at" > '2024-12-31 23:59:59.999999'

Или отзывы полученные после 10 февраля 2025 года

```python
from datetime import datetime
cutoff_date = datetime(2025, 2, 10)
Review.objects.filter(created_at__gt=cutoff_date)
Review.objects.filter(created_at__date__gt="2025-02-10")
```

WHERE django_datetime_cast_date("core_review"."created_at", 'UTC', 'UTC') > '2025-02-10'

## Варианты получить логическое И

Мы можем вызвать фильтры цепочкой, чтобы получить логическое И.
```Python
Service.objects.filter(name__contains='борода').filter(price__gt=200)
```

Мы можем в одном фильтре, указать условия для разных полей, чтобы получить логическое И.
Услуга где есть борода и цена выше 200
```python
Service.objects.filter(name__contains='борода', price__gt=200)
```

Мы можем вызвать фильтр к уже полученному результату, т.е. применить его к кверисету
```python
query = Service.objects.filter(name__contains='борода')
query = query.filter(price__gt=200)
```

## Q - объекты в Django ORM

Q - это объект, который позволяет создавать сложные запросы в Django ORM. Он используется для объединения нескольких фильтров в один запрос.

Q поддерживает логические операторы AND, OR и NOT.
- `()` - оператор группировки
- `~` - оператор NOT
- `&` - оператор AND
- `|` - оператор OR

```python
from django.db.models import Q

# Простой запрос с использованием Q и оператора AND
services = Service.objects.filter(
    Q(name__contains='бород') & Q(price__gt=200)
    )

# Мы можем создать Q отдлеьно
q1 = Q(name__contains='бород')
q2 = Q(price__gt=200)
services = Service.objects.filter(q1 & q2)

# Мы можем создать даже пустую Q и добавлять в нее условия
q = Q()
q &= Q(name__contains='бород')
q &= Q(price__gt=200)
services = Service.objects.filter(q)
```

#TODO Пояснения по запросам
- Рассказать про каждый из 3 запросов
- Рассказть про "инпплейс" операции

`&=` - это оператор, который объединяет два объекта Q, применяя оператор AND.
`|=` - это оператор, который объединяет два объекта Q, применяя оператор OR.
#TODO - как добавить NOT?

### Практика
С испольованием Q
1. Найти всех мастеров у которых имя начинается на букву А или заканчивается на букву а
2. Хорошие отзывы на Алевтину. Отзыв с оценкой больше 3 и имя мастера == Алевтина
3. Найти всех мастеров, у которых Имя начниается на букву А и мастер оказывает больше 1 услуги (тут можно использовать метод `count` у QuerySet)


```python
# 1.
from django.db.models import Q
a_masters = Master.objects.filter(
    Q(first_name__startswith='А') | ...
)

# 2.
q_mark = Q(rating__gte=3)
q_name = Q(...)
good_reviews = Review.objects.filter(q_mark & ...)


# 3. Плохое решение
# Получаем всех мастеров с именами на "А"
masters_starting_with_A = Master.objects.filter(first_name__startswith='А')

# Создаем список мастеров, у которых больше 1 услуги
result = [master for master in masters_starting_with_A if master.services.count() > 1]

# 3. Хорошее решение
# Получаем мастеров с именами на "А" и более чем одной услугой
result = Master.objects.filter(
    first_name__startswith='А'
).annotate(
    service_count=Count('services')
).filter(
    service_count__gt=1
)