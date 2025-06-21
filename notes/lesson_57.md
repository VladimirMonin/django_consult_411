# Тема Django ORM Ч4. LookUp и знакомство с Q. Урок 57 📚

## Наши модели 📝
Рассмотрим основные модели нашего приложения барбершопа. Они описывают ключевые сущности: мастеров, заказы, отзывы и услуги.

```python
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
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ["last_name", "first_name"]
```

Модель `Master` представляет мастеров барбершопа с основными полями: имя, фамилия, отчество, телефон, email и связь с услугами через `ManyToManyField`. Особенности:

- Поля `middle_name`, `email` могут быть пустыми (`null=True, blank=True`)
- Телефон имеет значение по умолчанию
- Метод `__str__` определяет строковое представление объекта

Теперь рассмотрим модель заказов, которая связана с мастерами:

```python
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
```

Модель `Order` хранит информацию о заказах клиентов. Ключевые особенности:

- Связь с мастером через `ForeignKey` (один мастер - много заказов)
- Связь с услугами через `ManyToManyField` (один заказ может включать несколько услуг)
- Поле `comment` необязательное (`null=True, blank=True`)
- При удалении мастера заказы остаются с `master=None` (`on_delete=models.SET_DEFAULT`)

Далее рассмотрим модель отзывов, которая позволяет клиентам оставлять оценки мастерам:

```python
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
```

Модель `Review` содержит отзывы клиентов с рейтингом (1-5), текстом, фотографией и флагом публикации. Особенности:

- Рейтинг реализован через `choices` с вариантами от 1 до 5
- Поле `photo` необязательное, загружается в папку `reviews/`
- Поле `is_published` определяет видимость отзыва на сайте
- Автоматически сохраняется дата создания (`auto_now_add=True`)

Теперь рассмотрим модель услуг, которые предоставляет барбершоп:

```python
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
```

Модель `Service` описывает услуги барбершопа с ценой, длительностью и флагом популярности. Особенности:

- Цена хранится как `DecimalField` для точности расчетов
- Длительность в минутах с подсказкой (`help_text`)
- Метод `__str__` возвращает название услуги

Теперь перейдем к основной теме урока - работе с LookUp и Q-объектами в Django ORM.

## Что такое LookUp? 🔍

Лукапы (LookUp) — это способ фильтрации данных в Django ORM. Они позволяют выполнять сложные запросы к базе данных, используя условные выражения и операторы. LookUp добавляются к именам полей через двойное подчеркивание `__` и определяют условия выборки.

Основные преимущества LookUp:

1. Позволяют создавать сложные условия фильтрации
2. Выполняются на стороне БД (эффективно)
3. Поддерживают все основные SQL-операторы

Рассмотрим базовый синтаксис LookUp на примере:

```python
from django.db.models import Q

# Фильтрация Заявок по имени мастера
orders = Order.objects.filter(master__first_name="Алевтина")
```

Синтаксис `master__first_name` означает:

- `master` - поле связи с моделью Master
- `first_name` - поле в связанной модели
- Двойное подчеркивание `__` указывает на переход по связи

Этот LookUp эквивалентен SQL-запросу с JOIN между таблицами заказов и мастеров.

### Примеры простых лукапов 💡

Для работы с LookUp удобно использовать Django shell. Запустим его с выводом SQL-запросов:

```python
poetry run python manage.py shell_plus --print-sql
```

Без LookUp нам пришлось бы выполнять два запроса - сначала найти мастера, затем его заказы. LookUp позволяет сделать это одним запросом:

```python
# Фильтрация Заявок по имени мастера
master = Master.objects.get(first_name="Алевтина")
orders = Order.objects.filter(master=master)

# Или даже в одну строку
aleftina_orders = Master.objects.get(first_name="Алевтина").orders.all()
```

### Таблица лукапов для условий выборки 📊

В Django доступно множество LookUp-операторов для разных типов условий. Рассмотрим основные из них:

| Lookup      | Описание                                                                                                                                     | Пример использования                                             |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| exact       | Точное совпадение значения (регистрозависимое для строк)                                                                                    | Master.objects.filter(first_name__exact='Алевтина')              |
| iexact      | Точное совпадение значения без учета регистра                                                                                               | Master.objects.filter(first_name__iexact='алевтина')             |
| contains    | Содержит заданную подстроку (регистрозависимое)                                                                                             | Service.objects.filter(name__contains='стрижка')                 |
| icontains   | Содержит заданную подстроку (без учета регистра)                                                                                            | Service.objects.filter(name__icontains='СТРИЖКА')                |
| in          | Значение поля находится в списке                                                                                                            | Master.objects.filter(id__in=[1, 2, 3])                         |
| gt          | Больше заданного значения                                                                                                                   | Service.objects.filter(price__gt=1000)                          |
| gte         | Больше или равно заданному значению                                                                                                         | Service.objects.filter(price__gte=1000)                         |
| lt          | Меньше заданного значения                                                                                                                   | Service.objects.filter(price__lt=1000)                          |
| lte         | Меньше или равно заданному значению                                                                                                         | Service.objects.filter(price__lte=1000)                         |
| startswith  | Начинается с заданной подстроки (регистрозависимое)                                                                                         | Master.objects.filter(last_name__startswith='Ив')                |
| istartswith | Начинается с заданной подстроки (без учета регистра)                                                                                        | Master.objects.filter(last_name__istartswith='ив')               |
| endswith    | Заканчивается на заданную подстроку (регистрозависимое)                                                                                    | Master.objects.filter(last_name__endswith='ов')                  |
| iendswith   | Заканчивается на заданную подстроку (без учета регистра)                                                                                   | Master.objects.filter(last_name__iendswith='ОВ')                 |
| range       | Находится в заданном диапазоне (включительно)                                                                                               | Service.objects.filter(price__range=(500, 2000))                 |
| date        | Соответствует заданной дате                                                                                                                 | Review.objects.filter(created_at__date=datetime.date(2025, 6, 1))|
| year        | Соответствует заданному году                                                                                                                | Review.objects.filter(created_at__year=2025)                     |
| month       | Соответствует заданному месяцу                                                                                                              | Review.objects.filter(created_at__month=6)                       |
| day         | Соответствует заданному дню                                                                                                                 | Review.objects.filter(created_at__day=1)                         |
| week_day    | Соответствует заданному дню недели (0 - понедельник, 6 - воскресенье)                                                                       | Review.objects.filter(created_at__week_day=0)                    |
| isnull      | Является NULL или не NULL                                                                                                                   | Master.objects.filter(middle_name__isnull=True)                  |
| regex       | Соответствует заданному регулярному выражению                                                                                               | Master.objects.filter(first_name__regex=r'^[А-Яа-я]+$')          |

## Практика с фильтрацией через лукапы 🛠️

Лукап - не всегда история про Join таблиц, как это было в первом примере. Это часто так же и работа в одной таблице где нам надо использовать логические операторы SQL.

Такие операторы как `IN`, `BETWEEN`, `LIKE` и т.д.

### Поиск услуг по названию

Найдем все услуги, в названии которых есть слово "борода". В SQL это соответствует оператору LIKE:

```python
query1 = Service.objects.filter(name__contains='бород')
```

Оператор `__contains` проверяет наличие подстроки в поле (регистрозависимый аналог SQL LIKE). Для регистронезависимого поиска используйте `__icontains`.

SQL-запрос будет выглядеть как: `WHERE "core_service"."name" LIKE '%бород%'`

### Фильтрация по списку значений

Для выборки мастеров с определенными ID используем оператор `__in`:

```python
query2 = Master.objects.filter(id__in=[1, 2, 3])
```

Оператор `__in` проверяет вхождение значения поля в указанный список. Это эквивалентно SQL-оператору IN.

SQL-запрос: `WHERE "core_master"."id" IN (1, 2, 3)`

### Фильтрация по числовым значениям

Для выборки услуг с ценой от 1000 рублей используем оператор `__gte` (greater than or equal):

```python
Service.objects.filter(price__gte=1000)
```

Оператор `__gte` проверяет, что значение поля больше или равно указанному. Аналогично:

- `__gt` - строго больше
- `__lt` - строго меньше
- `__lte` - меньше или равно

SQL-запрос: `WHERE "core_service"."price" >= 1000`

### Фильтрация по диапазону значений

Для выборки услуг в определенном ценовом диапазоне используем оператор `__range`:

```python
Service.objects.filter(price__range=(500, 2000))
```

Оператор `__range` проверяет вхождение значения в диапазон (включительно). Это эквивалентно SQL-оператору BETWEEN.

SQL-запрос: `WHERE "core_service"."price" BETWEEN 500 AND 2000`

### Фильтрация по окончанию строки

Для поиска мастеров с фамилией на "ый" используем оператор `__endswith`:

```python
Master.objects.filter(last_name__endswith='ый')
```

Оператор `__endswith` проверяет окончание строки (регистрозависимый). Для регистронезависимого варианта используйте `__iendswith`.

### Фильтрация по дате

Для выборки отзывов за 2025 год используем оператор `__year`:

```python
Review.objects.filter(created_at__year=2025)
```

Оператор `__year` извлекает год из даты и сравнивает его с заданным. Аналогично работают:

- `__month` - по месяцу
- `__day` - по дню

SQL-запрос: `WHERE "core_review"."created_at" BETWEEN '2025-01-01 00:00:00' AND '2025-12-31 23:59:59.999999'`

### Фильтрация по дате и времени 📅

Мы можем фильтровать записи по дате и времени, используя различные LookUp-операторы. Например, чтобы найти записи на услугу, созданные позже определенной даты:

```python
import datetime
Review.objects.filter(created_at__gt=datetime.date(2025, 1, 1))

# Или через __year
Review.objects.filter(created_at__year__gt=2024)
```

Эти запросы эквивалентны SQL-выражениям:
`WHERE "core_review"."created_at" > '2025-01-01 00:00:00'`
`WHERE "core_review"."created_at" > '2024-12-31 23:59:59.999999'`

Также можно фильтровать отзывы, полученные после конкретной даты, используя `datetime` объекты:

```python
from datetime import datetime
cutoff_date = datetime(2025, 2, 10)
Review.objects.filter(created_at__gt=cutoff_date)
Review.objects.filter(created_at__date__gt="2025-02-10")
```

SQL-запрос для второго примера: `WHERE django_datetime_cast_date("core_review"."created_at", 'UTC', 'UTC') > '2025-02-10'`

## Варианты получения логического И (AND) 🤝

В Django ORM есть несколько способов объединить условия фильтрации с помощью логического оператора И (AND).

### Цепочка фильтров

Мы можем последовательно вызывать метод `filter()`, чтобы объединить условия через AND. Каждый последующий `filter()` будет применяться к результатам предыдущего:

```python
Service.objects.filter(name__contains='борода').filter(price__gt=200)
```

### Несколько условий в одном фильтре

Другой способ - указать несколько условий в одном вызове `filter()`. Django автоматически объединит их через логическое И:

```python
Service.objects.filter(name__contains='борода', price__gt=200)
```

Этот подход более компактен и часто предпочтителен для простых комбинаций условий.

### Применение фильтра к QuerySet

Мы также можем применить фильтр к уже полученному QuerySet, что позволяет динамически строить запросы:

```python
query = Service.objects.filter(name__contains='борода')
query = query.filter(price__gt=200)
```

Этот метод полезен, когда условия фильтрации зависят от логики программы и добавляются пошагово.

## Q-объекты в Django ORM 🧩

Q-объекты (`django.db.models.Q`) предоставляют мощный и гибкий способ создания сложных запросов, включая логические операторы И (AND), ИЛИ (OR) и НЕ (NOT). Они позволяют объединять несколько фильтров в один запрос, что особенно полезно для построения динамических и сложных условий.

Основные логические операторы, поддерживаемые Q-объектами:

- `()` - оператор группировки (для определения порядка выполнения операций)
- `~` - оператор НЕ (NOT)
- `&` - оператор И (AND)
- `|` - оператор ИЛИ (OR)

Рассмотрим примеры использования Q-объектов:

```python
from django.db.models import Q

# Простой запрос с использованием Q и оператора AND
services = Service.objects.filter(
    Q(name__contains='бород') & Q(price__gt=200)
    )
```

В этом примере мы ищем услуги, в названии которых есть "бород" И цена которых больше 200.

```python
# Мы можем создать Q отдельно
q1 = Q(name__contains='бород')
q2 = Q(price__gt=200)
services = Service.objects.filter(q1 & q2)
```

Этот подход повышает читаемость кода, позволяя определить каждое условие отдельно.

```python
# Мы можем создать даже пустую Q и добавлять в нее условия
q = Q()
q &= Q(name__contains='бород')
q &= Q(price__gt=200)
services = Service.objects.filter(q)
```

Такой способ удобен для динамического построения запросов, когда условия добавляются в зависимости от входных данных или логики приложения.

### Три варианта Q-запросов 🔍

Рассмотрим три основных способа использования Q-объектов для построения запросов, каждый из которых имеет свои преимущества:

1. **Прямое использование Q в фильтре**:

```python
services = Service.objects.filter(
    Q(name__contains='бород') & Q(price__gt=200)
)
```

Этот вариант является наиболее компактным и удобен для формирования простых, но комбинированных условий непосредственно в вызове `filter()`.

2. **Создание отдельных Q-объектов**:

```python
q1 = Q(name__contains='бород')
q2 = Q(price__gt=200)
services = Service.objects.filter(q1 & q2)
```

Этот подход позволяет создавать и переиспользовать Q-объекты, что делает код более модульным и читаемым, особенно когда условия становятся сложнее или используются в нескольких местах.

3. **Постепенное построение Q-объекта**:

```python
q = Q()
q &= Q(name__contains='бород')
q &= Q(price__gt=200)
services = Service.objects.filter(q)
```

Этот метод обеспечивает максимальную гибкость для динамического построения запросов. Вы можете начать с пустого Q-объекта и добавлять к нему условия по мере необходимости, используя операторы `&=` или `|=`.

### In-place операции с Q 🛠️

Операторы `&=` (AND) и `|=` (OR) позволяют модифицировать существующие Q-объекты, добавляя к ним новые условия. Это очень удобно для постепенного формирования сложных запросов.

```python
q = Q(name__contains='бород')
q &= Q(price__gt=200)  # Добавляем условие по цене через AND
```

В этом примере к существующему условию `name__contains='бород'` добавляется новое условие `price__gt=200` с использованием логического И.

### Оператор NOT в Q ❗

Для отрицания условия в Q-объектах используется оператор `~`. Это позволяет легко исключать записи, соответствующие определенному критерию.

```python
# Найти услуги, где в названии нет "борода"
services = Service.objects.filter(~Q(name__contains='бород'))
```

Этот запрос вернет все услуги, в названии которых отсутствует подстрока "борода".

### Практика с Q-объектами 🏋️

Рассмотрим несколько практических задач, демонстрирующих мощь и гибкость Q-объектов в Django ORM.

### Задача 1: Мастера с именами на "А" или заканчивающимися на "а"

Нам нужно найти всех мастеров, чье имя начинается на букву "А" или заканчивается на "а". Здесь идеально подходит оператор логического ИЛИ (`|`).

```python
from django.db.models import Q

a_masters = Master.objects.filter(
    Q(first_name__startswith='А') | Q(first_name__endswith='а')
)
```

В этом примере мы используем оператор `|` для объединения двух условий: `first_name__startswith='А'` и `first_name__endswith='а'`. Django ORM преобразует это в соответствующий SQL-запрос с `OR`.

### Задача 2: Хорошие отзывы на Алевтину

Требуется найти все отзывы, которые имеют рейтинг 3 или выше И относятся к мастеру по имени "Алевтина". Здесь мы используем оператор логического И (`&`).

```python
from django.db.models import Q

good_reviews = Review.objects.filter(
    Q(rating__gte=3) &
    Q(master__first_name='Алевтина')
)
```

Мы комбинируем условия через `&` (AND) для поиска отзывов с рейтингом больше или равным 3 и связанных с мастером по имени "Алевтина". Обратите внимание на использование LookUp `master__first_name` для доступа к полю связанной модели.

### Задача 3: Мастера на "А" с более чем 1 услугой

Эта задача требует более сложного подхода: сначала отфильтровать мастеров по имени, затем подсчитать количество их услуг и, наконец, отфильтровать тех, у кого услуг больше одной.

```python
from django.db.models import Q, Count

result = Master.objects.filter(
    first_name__startswith='А'
).annotate(
    service_count=Count('services')
).filter(
    service_count__gt=1
)
```

Это оптимальное решение с использованием `annotate()` и `Count()` для подсчета услуг у каждого мастера. `annotate()` добавляет временное поле `service_count` к каждому объекту `Master`, которое затем используется для фильтрации.

>[!info]
>
>#### Оптимизация запросов 🚀
>
>Вариант с `annotate()` и `Count()` более эффективен, чем попытка фильтрации в Python после получения всех данных. Это связано с тем, что вся работа по подсчету и фильтрации выполняется на стороне базы данных, что значительно снижает объем передаваемых данных и нагрузку на приложение.
