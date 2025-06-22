# Тема Django ORM Ч5. Annotate. Жадные запросы. Поисковая форма. Урок 58

## Annotate - добавление агрегированных данных к объектам

### Что такое annotate?

**annotate в Django ORM** — это мощный метод, который позволяет добавлять агрегированные (вычисленные) поля к каждому объекту в наборе запросов (QuerySet). Это означает, что вы можете выполнять сложные вычисления, такие как подсчет, суммирование, усреднение или нахождение максимума/минимума связанных данных, и прикреплять результат этих вычислений непосредственно к каждому объекту основной модели.

Давайте разберем это подробнее, используя примеры из файла notes/lesson_58.md:



Метод `annotate()` используется для добавления к каждому объекту в QuerySet нового поля, которое является результатом агрегационной функции. Это поле не существует в базе данных изначально, оно вычисляется "на лету" во время выполнения запроса.

Основная идея: Вы берете набор объектов (например, всех Master'ов) и для каждого из них вычисляете какую-то сводную информацию из связанных объектов (например, количество Order'ов, средний Review и т.д.).


### Зачем использовать annotate?

Эффективность: Вместо того чтобы выполнять отдельные запросы к базе данных для каждого объекта (что приводит к проблеме N+1 запросов), annotate позволяет получить все необходимые агрегированные данные за один запрос к базе данных. Это значительно повышает производительность.
Удобство: Агрегированные данные становятся доступны как обычные атрибуты объектов, что упрощает их использование в шаблонах или логике приложения.
Гибкость: Можно комбинировать различные агрегационные функции, фильтры и сортировки для получения очень специфичных данных.

### Как работает annotate?
Вы вызываете метод annotate() на QuerySet'е вашей модели и передаете ему именованные аргументы, где имя аргумента становится именем нового поля, а значение — агрегационной функцией.

Синтаксис:
Модель.objects.annotate(новое_поле=АгрегационнаяФункция('связанное_поле'))

Пример 1: Подсчёт количества заказов у каждого мастера (из notes/lesson_58.md:14)

from django.db.models import Count

masters_with_order_count = Master.objects.annotate(
    order_count=Count('orders')  # 'orders' - это related_name для ForeignKey из Order к Master
)

python


Здесь:

Master.objects — это QuerySet всех объектов Master.
annotate() — метод, который добавляет новое поле.
order_count — это имя нового поля, которое будет добавлено к каждому объекту Master.
Count('orders') — агрегационная функция, которая подсчитывает количество связанных объектов Order. Предполагается, что в модели Order есть ForeignKey на Master, и related_name для этого отношения установлен как orders (или Django автоматически создает его как order_set).
После выполнения этого запроса, каждый объект master в masters_with_order_count будет иметь атрибут master.order_count.

Распространенные агрегационные функции, используемые с annotate:
Файл notes/lesson_58.md демонстрирует использование нескольких ключевых агрегационных функций:

Count: Подсчитывает количество объектов.

Пример: Count('orders') (количество заказов), Count('review') (количество отзывов).
Может использоваться с distinct=True для подсчета уникальных значений, например: Count('orders__phone', distinct=True) (количество уникальных клиентов по номеру телефона, см. notes/lesson_58.md:175).
Может использоваться с filter для условного подсчета, например: Count('services', filter=Q(services__is_popular=True)) (количество популярных услуг, см. notes/lesson_58.md:95).
Avg: Вычисляет среднее значение.

Пример: Avg('review__rating') (средний рейтинг мастера, см. notes/lesson_58.md:35), Avg('services__duration') (средняя длительность услуг, см. notes/lesson_58.md:115).
Sum: Вычисляет сумму значений.

Пример: Sum('orders__services__price') (общая сумма заказов, см. notes/lesson_58.md:75), Sum('orders__services__duration') (общая длительность заказов, см. notes/lesson_58.md:155).
Max: Находит максимальное значение.

Пример: Max('review__rating') (максимальный рейтинг, см. notes/lesson_58.md:235).
Комбинирование annotate с другими методами QuerySet:
order_by(): Результаты annotate часто сортируются по новым агрегированным полям.
Пример: .order_by('-order_count') (сортировка по убыванию количества заказов, см. notes/lesson_58.md:16).
filter(): Можно применять фильтры до или после annotate. Если фильтр применяется внутри annotate (как в примерах с Q объектами), он влияет только на агрегацию для этого конкретного поля.
Пример: Count('review', filter=Q(review__is_published=True)) (подсчет только опубликованных отзывов, см. notes/lesson_58.md:135).
Множественная аннотация: Вы можете добавить несколько агрегированных полей в одном вызове annotate().
Пример: total_services=Count('services', distinct=True), total_orders=Count('orders', distinct=True) (общее количество услуг и заказов, см. notes/lesson_58.md:298-299).

Вот 15 учебных примеров ORM-запросов с использованием `annotate` для вашей системы, с **максимально подробными** описаниями. Запросы идут от простых к сложным.

---
## Примеры использования annotate

Запустим shell plus `poetry run python manage.py shell_plus --print-sql` и будем выполнять запросы.

### **1. Подсчёт количества заказов у каждого мастера**

**Описание**:  
Этот запрос добавляет к каждому объекту `Master` новое поле `order_count`, которое содержит общее количество заказов, связанных с этим мастером через `ForeignKey` в модели `Order`. Используется агрегационная функция `Count`.

**Запрос**:
```python
from django.db.models import Count

masters_with_order_count = Master.objects.annotate(
    order_count=Count('orders')  # Считаем количество заказов для каждого мастера
).order_by('-order_count')  # Сортируем по убыванию количества заказов

# Использование
for master in masters_with_order_count:
    print(f"Мастер: {master.last_name} {master.first_name}, Заказов: {master.order_count}")

# Или просто вытащить количество заявок мастера [0]
print(masters_with_order_count[0].order_count)
```
---

### **2. Средний рейтинг мастера на основе отзывов**

**Описание**:  
Для каждого мастера вычисляется средний рейтинг (`avg_rating`) на основе оценок из связанных отзывов (`Review`). Используется агрегационная функция `Avg`. Результат сортируется по убыванию среднего рейтинга.

**Запрос**:
```python
from django.db.models import Avg

masters_with_avg_rating = Master.objects.annotate(
    avg_rating=Avg('review__rating')  # Вычисляем средний рейтинг
).order_by('-avg_rating')  # Сортируем по убыванию рейтинга

# Использование

for master in masters_with_avg_rating:
    # Если у некоторых не будет отзывов TypeError: unsupported format string passed to NoneType.__format__ потому что None не поддерживает форматирование)
    print(f"Мастер: {master.last_name}, Средний рейтинг: {master.avg_rating:.2f}")
```
---

### **3. Количество отзывов для каждого мастера**

**Описание**:  
Добавляет поле `review_count`, содержащее количество отзывов, оставленных для каждого мастера. Используется агрегационная функция `Count`.

**Запрос**:
```python
python
from django.db.models import Count

masters_with_review_count = Master.objects.annotate(
    review_count=Count('review')  # Считаем количество отзывов
).order_by('-review_count')  # Сортируем по убыванию количества отзывов

# Использование

for master in masters_with_review_count:
    print(f"Мастер: {master.last_name}, Отзывов: {master.review_count}")
```
---

### **4. Общая сумма заказов для каждого мастера**

**Описание**:  
Для каждого мастера вычисляется общая сумма (`total_order_price`) всех услуг в его заказах. Используется агрегационная функция `Sum` через связанные модели `Order` и `Service`.

**Запрос**:
```python
from django.db.models import Sum

masters_with_total_price = Master.objects.annotate(
    total_order_price=Sum('orders__services__price')  # Суммируем цены услуг
).order_by('-total_order_price')

# Использование

for master in masters_with_total_price:
    print(f"Мастер: {master.last_name}, Общая сумма заказов: {master.total_order_price}")
```
---

### **5. Количество популярных услуг у каждого мастера**

**Описание**:  
Подсчитывает количество популярных услуг (`is_popular=True`), связанных с каждым мастером. Используется агрегация `Count` с фильтром.

**Запрос**:
```python
from django.db.models import Count, Q

masters_with_popular_services = Master.objects.annotate(
    popular_service_count=Count('services', filter=Q(services__is_popular=True))
).order_by('-popular_service_count')

# Использование

for master in masters_with_popular_services:
    print(f"Мастер: {master.last_name}, Популярных услуг: {master.popular_service_count}")
```
---

### **6. Средняя длительность услуг мастера**

**Описание**:  
Для каждого мастера вычисляется средняя длительность (`avg_duration`) его услуг в минутах. Используется `Avg`.

**Запрос**:
```python
from django.db.models import Avg

masters_with_avg_duration = Master.objects.annotate(
    avg_duration=Avg('services__duration')
).order_by('-avg_duration')

# Использование

for master in masters_with_avg_duration:
    print(f"Мастер: {master.last_name}, Средняя длительность услуг: {master.avg_duration} мин.")
```
---

### **7. Количество опубликованных отзывов для мастера**

**Описание**:  
Подсчитывает только опубликованные отзывы (`is_published=True`) для каждого мастера. Используется `Count` с фильтром.

**Запрос**:
```python
from django.db.models import Count, Q

masters_with_published_reviews = Master.objects.annotate(
    published_review_count=Count('review', filter=Q(review__is_published=True))
).order_by('-published_review_count')

# Использование

for master in masters_with_published_reviews:
    print(f"Мастер: {master.last_name}, Опубликованных отзывов: {master.published_review_count}")
```
---

### **8. Общая длительность всех заказов мастера**

**Описание**:  
Вычисляет общее время (`total_order_duration`), которое мастер затратил на все свои заказы (сумма длительностей услуг).

**Запрос**:
```python
from django.db.models import Sum

masters_with_total_duration = Master.objects.annotate(
    total_order_duration=Sum('orders__services__duration')
).order_by('-total_order_duration')

# Использование

for master in masters_with_total_duration:
    print(f"Мастер: {master.last_name}, Общее время заказов: {master.total_order_duration} мин.")
```

### **8.1 Общая длительность всех заказов мастера за конкретный месяц**

**Описание**:
Вариация предыдущего запроса с фильтрацией по дате. Вычисляет общее время (`total_order_duration_month`), которое мастер затратил на заказы за конкретный месяц. Используется `Sum` с фильтром по полю `created_at`.

**Запрос**:
```python
from django.db.models import Sum, Q
from datetime import datetime

# Выбираем год и месяц для фильтрации
year = 2023
month = 5  # Май

masters_with_monthly_duration = Master.objects.annotate(
    total_order_duration_month=Sum(
        'orders__services__duration',
        filter=Q(orders__created_at__year=year, orders__created_at__month=month)
    )
).order_by('-total_order_duration_month')

# Использование
for master in masters_with_monthly_duration:
    print(f"Мастер: {master.last_name}, Время заказов за {month}/{year}: {master.total_order_duration_month or 0} мин.")
```

**Примечания**:
- Если у мастера не было заказов в указанный месяц, значение будет `None`, поэтому используем `or 0` при выводе
- Можно динамически задавать год и месяц через переменные
- Фильтр по дате применяется только к агрегируемым данным, не затрагивая основную выборку мастеров

---

### **9. Количество уникальных клиентов у мастера**

**Описание**:  
Подсчитывает количество уникальных клиентов (`unique_clients`), оставивших заказы у мастера. Используется `Count` с `distinct=True`.

**Запрос**:
```python
from django.db.models import Count

masters_with_unique_clients = Master.objects.annotate(
    unique_clients=Count('orders__phone', distinct=True)  # Уникальные номера телефонов
).order_by('-unique_clients')

# Использование

for master in masters_with_unique_clients:
    print(f"Мастер: {master.last_name}, Уникальных клиентов: {master.unique_clients}")
```
---

### **10. Средняя цена услуг мастера**

**Описание**:  
Для каждого мастера вычисляется средняя цена (`avg_service_price`) его услуг. Используется `Avg`.

**Запрос**:
python
from django.db.models import Avg

masters_with_avg_price = Master.objects.annotate(
    avg_service_price=Avg('services__price')
).order_by('-avg_service_price')

# Использование

for master in masters_with_avg_price:
    print(f"Мастер: {master.last_name}, Средняя цена услуг: {master.avg_service_price:.2f}")

---

### **11. Количество заказов с комментариями**

**Описание**:  
Подсчитывает количество заказов (`orders_with_comments`), у которых есть комментарии (не `NULL` и не пустые). Используется `Count` с фильтром.

**Запрос**:
python
from django.db.models import Count, Q

masters_with_commented_orders = Master.objects.annotate(
    orders_with_comments=Count('orders', filter=Q(orders__comment__isnull=False) & ~Q(orders__comment=''))
).order_by('-orders_with_comments')

# Использование

for master in masters_with_commented_orders:
    print(f"Мастер: {master.last_name}, Заказов с комментариями: {master.orders_with_comments}")

---

### **12. Максимальный рейтинг среди отзывов мастера**

**Описание**:  
Находит максимальную оценку (`max_rating`), которую получал мастер. Используется `Max`.

**Запрос**:
python
from django.db.models import Max

masters_with_max_rating = Master.objects.annotate(
    max_rating=Max('review__rating')
).order_by('-max_rating')

# Использование

for master in masters_with_max_rating:
    print(f"Мастер: {master.last_name}, Максимальная оценка: {master.max_rating}")

---

### **13. Количество услуг с длительностью более 30 минут**

**Описание**:  
Подсчитывает количество услуг (`long_services`), длительность которых превышает 30 минут. Используется `Count` с фильтром.

**Запрос**:
python
from django.db.models import Count, Q

masters_with_long_services = Master.objects.annotate(
    long_services=Count('services', filter=Q(services__duration__gt=30))
).order_by('-long_services')

# Использование

for master in masters_with_long_services:
    print(f"Мастер: {master.last_name}, Услуг >30 мин: {master.long_services}")

---

### **14. Средний рейтинг мастера за последний месяц**

**Описание**:  
Вычисляет средний рейтинг (`avg_rating_last_month`) только для отзывов, созданных за последние 30 дней. Используется `Avg` с фильтром по дате.

**Запрос**:
```python
from django.db.models import Avg, Q
from datetime import datetime, timedelta

last_month = datetime.now() - timedelta(days=30)

masters_with_recent_avg_rating = Master.objects.annotate(
    avg_rating_last_month=Avg('review__rating', filter=Q(review__created_at__gte=last_month))
).order_by('-avg_rating_last_month')

# Использование

for master in masters_with_recent_avg_rating:
    print(f"Мастер: {master.last_name}, Средний рейтинг за месяц: {master.avg_rating_last_month:.2f}")
```
---

### **15. Общее количество услуг и заказов для мастера**

**Описание**:  
Добавляет два поля: общее количество услуг (`total_services`) и заказов (`total_orders`) для каждого мастера. Используется множественная агрегация.

**Запрос**:
```python
from django.db.models import Count

masters_with_totals = Master.objects.annotate(
    total_services=Count('services', distinct=True),
    total_orders=Count('orders', distinct=True)
).order_by('-total_orders', '-total_services')

# Использование

for master in masters_with_totals:
    print(f"Мастер: {master.last_name}, Услуг: {master.total_services}, Заказов: {master.total_orders}")
```
---

Каждый пример включает:

1. **Подробное описание** логики запроса.
2. **Код** с аннотацией и сортировкой.
3. **Пример использования** для вывода результатов.  

Если нужно углубиться в какой-то запрос или добавить новые — дайте знать!
