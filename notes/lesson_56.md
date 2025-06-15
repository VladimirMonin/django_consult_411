# Тема Django ORM Ч3. Связи «многие-ко-многим», расширение моделей. Урок 56

## Создание модели Отзыва

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
        verbose_name="Оценка", choices=RATING_CHOICES, default=5)
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
```

### Что такое choices?

- Что это?
- Какие варианты по типам данных?
- Как организовать choices?
- Может ли быть несколько полей с choices в одной модели?


### Что такое ImageField и почему нужен Pillow?

- Что за поле
- Как оно работает
- Почему нужен Pillow?

### Как настроить пути для image field?

- Какие вообще константы есть, за что они отвечают
- MEDIA_ROOT
- MEDIA_URL
- Настройки в urls.py
- Создаем папку `media`
- Добавляем папку `media` в `.gitignore`

### Как получить в шаблоне доступ к изображению?

- Что такое `{{ object.photo.url }}`
- Пример в шаблоне (кратко)

## Модель `Service`

```python
class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(
        verbose_name="Длительность", help_text="Время выполнения в минутах", default=20
    )
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
```
- Подключение модели в админке!
- Описание модели и ее полей
- Почему для duration в этом случае используем числовое поле а не DurationField?

## Выстраивание связей M2M

- Поля `Master.services` и `Order.services`

```python
services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="masters")
services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="orders")
```

- Как это работает?
- Что такое `related_name`?
- Django создаст автоматически промежуточные таблицы
- А что если мы хотим в связке Мастер - Услуга хранить комментарий или альтернативную цену?

## Запросы к M2M

Сейчас полная версия моделей выглядит так:

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
```

### Практика с запросами к M2M

Запускаем `shell plus` в режиме `--print-sql`

```python
poetry run python manage.py shell_plus --print-sql
```

Создадим запись на услугу. В первую очередь, добудем мастера и услуги
```python
master = Master.objects.get(pk=3)
services = Service.objects.all()
service_1 = services[0]
service_2 = services[1]
```

Создаем запись на услугу и добавляем две услуги
```python
order = Order.objects.create(master=master, name="Легалас", comment="Покраска в блонд",phone="1234567890")
order.services.add(service_1, service_2)
```

Получим последнюю запись на услугу и выведем все услуги, которые в ней есть
```python
last_order = Order.objects.last()
last_order.services
# <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x0000024A7C732660>
services_in_last_order = last_order.services.all()
```

Мы можем работать с M2M полем как с менеджером. В переменной `services_in_last_order` у нас QuerySet с услугами. Можем сделать обход циклом или добыть одну из услуг.

```python
[service.name for service in services_in_last_order]
# ['Стрижка бороды', 'Покраска бровей']
```
После запроса выше, мы сделали обход всех услуг и вывели их названия. Однако Django ORM ленив, и на самом деле НЕ выгружал все услуги из БД с первого раза. Поэтому у нас получилось несколько запросов. 

1. `Order.objects.last()` – выгружает последнюю запись на услугу
2.  `last_order.services.all()` – выгружает данные о записях в промежуточной таблице
3.  `service.name` – выгружает данные об услугах - для каждой услуги отдельный запрос

Удалим услугу из записи на услугу метод `remove`

```python
service_1 = Service.objects.get(pk=1)
last_order = Order.objects.last()
last_order.services.remove(service_1)
```

Мы можем очистить все связи методом `clear`
```python
last_order.services.clear()

```


Django предоставляет мощные инструменты для работы со связями "многие-ко-многим" (Many-to-Many). Это позволяет одной записи из одной модели быть связанной со множеством записей из другой модели, и наоборот.

### 1. Определение ManyToManyField

Для создания связи "многие-ко-многим" используется `models.ManyToManyField`. Это поле обычно определяется в одной из двух связанных моделей. Django автоматически создает промежуточную таблицу для управления этими связями.

**Пример:**
Если у вас есть модели `Master` и `Service`, и один мастер может предоставлять множество услуг, а одна услуга может быть предоставлена множеством мастеров, вы можете определить `ManyToManyField` следующим образом:

```python
from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    # ... другие поля

    def __str__(self):
        return self.name

class Master(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="masters")
    # ... другие поля

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```
В этом примере поле `services` в модели `Master` создает связь "многие-ко-многим" с моделью `Service`.

### 2. Автоматическая промежуточная таблица

Когда вы используете `ManyToManyField` без указания параметра `through`, Django автоматически создает промежуточную таблицу в базе данных. Эта таблица содержит два столбца: один для первичного ключа первой модели и один для первичного ключа второй модели, образуя составной уникальный ключ.

Например, для связи `Master` и `Service` Django создаст таблицу, которая может называться `core_master_services` (по умолчанию `appname_modelname_fieldname`), содержащую `master_id` и `service_id`.

### 3. Использование `through` модели для дополнительных полей

Иногда вам может потребоваться хранить дополнительную информацию о самой связи. Например, если мастер предоставляет услугу, возможно, вы захотите указать "альтернативную цену" или "комментарий" к этой конкретной услуге, предоставляемой этим мастером. В таких случаях вы можете определить свою собственную промежуточную модель (также известную как "through" модель).

**Пример с `through` моделью:**
Предположим, мы хотим хранить `price_for_master` (цена услуги для конкретного мастера) и `notes` (заметки) для каждой связи между `Master` и `Service`.

```python
from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    # ... другие поля

    def __str__(self):
        return self.name

class Master(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    # Указываем нашу промежуточную модель 'MasterService'
    services = models.ManyToManyField("Service", through='MasterService', verbose_name="Услуги")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class MasterService(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price_for_master = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена для мастера", null=True, blank=True)
    notes = models.TextField(verbose_name="Заметки", null=True, blank=True)

    class Meta:
        unique_together = ('master', 'service') # Гарантируем уникальность пары мастер-услуга

    def __str__(self):
        return f"{self.master.first_name} - {self.service.name}"
```
В этом случае `ManyToManyField` в модели `Master` указывает на `MasterService` как на промежуточную модель с помощью параметра `through`.

**Когда использовать `through` модель:**
*   Когда вам нужно хранить дополнительные данные о самой связи (например, дата начала/окончания, роль, количество, цена).
*   Когда вам нужна более сложная логика для управления связью (например, пользовательские методы сохранения или валидации для связи).

**Когда не использовать `through` модель (использовать автоматическую):**
*   Когда вам нужна простая связь "многие-ко-многим" без каких-либо дополнительных атрибутов. Это самый распространенный и простой вариант.

### 4. Управление связями Many-to-Many (API)

Django предоставляет менеджер для управления связями "многие-ко-многим" через атрибут `ManyToManyField`. Этот менеджер позволяет добавлять, удалять, устанавливать и очищать связанные объекты.

Предположим, у нас есть `master` (экземпляр `Master`) и `service_1`, `service_2` (экземпляры `Service`).

*   **`add(*objects)`**: Добавляет указанные объекты к набору связанных объектов. Если объект уже связан, он не будет добавлен повторно.

    ```python
    master.services.add(service_1)
    master.services.add(service_2, service_3) # Можно добавить несколько объектов
    ```

*   **`remove(*objects)`**: Удаляет указанные объекты из набора связанных объектов.

    ```python
    master.services.remove(service_1)
    ```

*   **`clear()`**: Удаляет все связанные объекты из набора.

    ```python
    master.services.clear() # Мастер больше не предоставляет никаких услуг
    ```

*   **`set(iterable, *, clear=False)`**: Заменяет текущий набор связанных объектов на указанный `iterable`.
    *   Если `clear=True` (по умолчанию `False`), то все существующие связи будут удалены перед добавлением новых.
    *   Если `clear=False`, то будут добавлены только новые связи, а существующие останутся.

    ```python
    # Заменяет все услуги мастера на service_4 и service_5
    master.services.set([service_4, service_5])

    # Добавляет service_6, сохраняя service_4 и service_5
    master.services.set([service_4, service_5, service_6], clear=False)
    ```

*   **`create(**kwargs)`**: Создает новый объект и немедленно связывает его с текущим объектом. Возвращает созданный объект.

    ```python
    # Создает новую услугу и связывает ее с мастером
    new_service = master.services.create(name="Новая услуга", price=100.00, duration=60)
    ```

*   **`through_defaults` (для `through` моделей)**: При использовании `through` модели, методы `add()`, `create()`, `set()` могут принимать аргумент `through_defaults`, который позволяет указать значения для полей промежуточной модели.

    ```python
    # Добавление услуги с указанием цены для мастера и заметок
    master.services.add(service_1, through_defaults={'price_for_master': 50.00, 'notes': 'Особые условия'})

    # Создание услуги и связи с ней, указывая данные для промежуточной модели
    new_service_with_details = master.services.create(
        name="Услуга с деталями",
        price=120.00,
        duration=90,
        through_defaults={'price_for_master': 60.00, 'notes': 'Важная услуга'}
    )
    ```

### 5. `related_name`

Параметр `related_name` в `ManyToManyField` (и `ForeignKey`) определяет имя обратной связи от связанной модели. Если `related_name` не указан, Django автоматически генерирует его (обычно `имя_модели_set`).

**Пример:**
В модели `Master` поле `services` имеет `related_name="masters"`. Это означает, что из объекта `Service` вы можете получить доступ ко всем связанным `Master` объектам через `service.masters.all()`.

```python
class Master(models.Model):
    # ...
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="masters")

class Order(models.Model):
    # ...
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="orders")

# Получить всех мастеров, предоставляющих service_1
masters_for_service_1 = service_1.masters.all()

# Получить все заказы, включающие service_1
orders_with_service_1 = service_1.orders.all()
```
`related_name` очень полезен для ясности кода и избежания конфликтов имен, особенно когда у одной модели есть несколько связей с другой моделью.

### 6. Запросы к Many-to-Many связям

Вы можете фильтровать объекты на основе их Many-to-Many связей.

**Примеры запросов:**

*   **Получить всех мастеров, которые предоставляют услугу с `pk=1`:**
    ```python
    masters_with_service_1 = Master.objects.filter(services__pk=1)
    ```
*   **Получить все услуги, которые предоставляет конкретный мастер:**
    ```python
    master = Master.objects.get(pk=3)
    services_of_master = master.services.all()
    ```
*   **Получить все заказы, которые включают услугу с названием "Стрижка бороды":**
    ```python
    orders_with_beard_trim = Order.objects.filter(services__name="Стрижка бороды")
    ```
*   **Использование `prefetch_related` для оптимизации запросов:**
    Когда вы обращаетесь к связанным объектам в цикле, это может привести к проблеме N+1 запросов. `prefetch_related` решает эту проблему, загружая все связанные объекты за один дополнительный запрос.

    ```python
    # Без prefetch_related: для каждого мастера будет отдельный запрос к услугам
    masters = Master.objects.all()
    for master in masters:
        print(f"{master.first_name}: {[s.name for s in master.services.all()]}")

    # С prefetch_related: услуги для всех мастеров будут загружены одним запросом
    masters = Master.objects.prefetch_related('services').all()
    for master in masters:
        print(f"{master.first_name}: {[s.name for s in master.services.all()]}")
    ```

### Рекомендации:

*   **Для простых связей:** Используйте `models.ManyToManyField` без параметра `through`. Это самый простой и эффективный способ.
*   **Для связей с дополнительными данными:** Определите явную промежуточную модель (`through` модель) и используйте ее в `ManyToManyField`.
*   **Используйте `related_name`:** Всегда указывайте `related_name` для ясности и предотвращения конфликтов, особенно в сложных моделях.
*   **Оптимизация запросов:** При выборке объектов, которые будут использоваться для доступа к связанным Many-to-Many объектам, всегда используйте `prefetch_related()` для избежания проблемы N+1 запросов и повышения производительности.
*   **Управление связями:** Используйте методы `add()`, `remove()`, `clear()`, `set()` для манипулирования связями. Избегайте прямого изменения промежуточной таблицы, если это не абсолютно необходимо.

Надеюсь, это подробное объяснение поможет вам в работе с Many-to-Many связями в Django!
