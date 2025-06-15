# Тема Django ORM Ч3. Связи «многие-ко-многим», расширение моделей. Урок 56

## Создание модели Отзыва 📝

Модель `Review` предназначена для хранения отзывов клиентов о работе мастеров. Она включает несколько ключевых полей, которые позволяют гибко управлять отзывами в системе. Основное текстовое содержание отзыва хранится в поле `text`, а имя клиента (необязательное поле) - в `client_name`.

Связь с моделью мастера осуществляется через `ForeignKey` в поле `master`, что позволяет легко находить все отзывы конкретного мастера. Для прикрепления фотографий используется поле `photo`, а оценка от 1 до 5 с текстовыми описаниями хранится в поле `rating`. Флаг публикации отзыва управляется полем `is_published`, позволяя скрывать нежелательные отзывы.

>[!info]
>#### Особенности модели Review
>- Использует `ImageField` для хранения фотографий (требует Pillow)
>- Имеет поле с выбором (`choices`) для оценки
>- Связана с моделью `Master` через ForeignKey

Вот полный код модели:

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

### Что такое choices? 📝

Поле с `choices` в Django позволяет ограничить возможные значения поля определенным набором вариантов. В нашем примере поле `rating` использует `RATING_CHOICES` для выбора оценки от 1 до 5 с соответствующими текстовыми описаниями.

```python
RATING_CHOICES = [
    (1, "Ужасно"),
    (2, "Плохо"),
    (3, "Нормально"),
    (4, "Хорошо"),
    (5, "Отлично"),
]
rating = models.PositiveSmallIntegerField(
    verbose_name="Оценка", choices=RATING_CHOICES, default=5
)
```

>[!info]
>#### Особенности использования choices
>- Первый элемент в кортеже - это значение, которое будет сохранено в базе данных
>- Второй элемент - человекочитаемое описание, которое отображается в интерфейсе
>- Можно использовать с разными типами полей: `CharField`, `IntegerField` и др.

В одной модели может быть несколько полей с `choices`. Например, мы могли бы добавить поле для выбора типа отзыва:

```python
REVIEW_TYPE_CHOICES = [
    ('text', 'Текстовый'),
    ('video', 'Видео'),
    ('photo', 'Фото'),
]
review_type = models.CharField(
    max_length=10, choices=REVIEW_TYPE_CHOICES, default='text'
)
```


### Что такое ImageField и почему нужен Pillow? 📷

`ImageField` - это специальное поле Django для работы с изображениями. Оно наследуется от `FileField` и добавляет проверку, что загруженный файл является изображением.

ImageField обладает несколькими важными особенностями. Во-первых, оно автоматически проверяет, что загруженный файл действительно является изображением, что предотвращает загрузку некорректных файлов. Во-вторых, поле поддерживает дополнительные атрибуты, такие как `height`, `width` и `upload_to`, которые позволяют контролировать размеры изображения и путь его сохранения. Важно отметить, что для работы ImageField требуется установка библиотеки `Pillow`, которая обеспечивает обработку изображений на Python.

>[!warning]
>#### Почему нужен Pillow?
>Библиотека `Pillow` требуется для:
>- Проверки, что файл действительно является изображением
>- Возможности получения размеров изображения (ширина/высота)
>- Опционального ресайза изображений при загрузке

Пример использования с дополнительными параметрами:
```python
photo = models.ImageField(
    upload_to='reviews/%Y/%m/%d/',  # Паттерн для пути сохранения
    width_field='image_width',      # Поле для хранения ширины
    height_field='image_height',    # Поле для хранения высоты
    blank=True,
    null=True
)
image_width = models.PositiveIntegerField(blank=True, null=True)
image_height = models.PositiveIntegerField(blank=True, null=True)
```

### Как настроить пути для image field? ⚙️

Для работы с загружаемыми файлами в Django нужно настроить несколько параметров:

Для корректной работы с загружаемыми файлами в Django необходимо выполнить настройки в двух файлах. В файле `settings.py` мы определяем базовые параметры: `MEDIA_ROOT` указывает физический путь к папке для хранения медиафайлов (обычно это поддиректория `media` в корне проекта), а `MEDIA_URL` задает URL-префикс для доступа к этим файлам через веб-интерфейс.

В файле `urls.py` проекта необходимо добавить специальную настройку, которая позволяет Django обслуживать медиафайлы в режиме разработки. Это делается путем добавления `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` к списку urlpatterns. Важно отметить, что в production-окружении эту функцию должен выполнять веб-сервер (Nginx или Apache).

>[!info]
>#### Практические шаги
>Для настройки работы с медиафайлами необходимо создать папку `media` в корне проекта и добавить `media/` в `.gitignore`. Также важно убедиться, что сервер имеет права на запись в эту папку для корректного сохранения загружаемых файлов.

При такой настройке изображения будут сохраняться в подпапках внутри `media/`, а доступ к ним будет по URL вида `/media/reviews/2023/10/photo.jpg`.

### Как получить в шаблоне доступ к изображению? 🖼️

Для отображения загруженного изображения в шаблоне используется `{{ object.photo.url }}`, который возвращает относительный URL изображения.

Пример шаблона:
```html
{% if object.photo %}
    <img src="{{ object.photo.url }}" alt="Фото отзыва" class="review-photo">
{% endif %}
```

>[!warning]
>#### Важные моменты
>При работе с изображениями в шаблонах всегда проверяйте наличие фото через `{% if %}` перед обращением к `.url`. Для корректной работы необходимо убедиться, что в настройках проекта правильно указаны `MEDIA_URL` и `MEDIA_ROOT`. В production-окружении требуется дополнительная настройка отдачи медиа-файлов через веб-сервер (Nginx или Apache).

Для получения дополнительной информации о фото можно использовать:
```html
<p>Размер: {{ object.photo.width }}x{{ object.photo.height }}px</p>
<p>Имя файла: {{ object.photo.name }}</p>
```

## Модель `Service` 💼

Модель `Service` представляет услугу, которую предоставляют мастера. Основные поля модели:

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

>[!info]
>#### Особенности полей модели
>- `name`: Обязательное поле с ограничением длины (200 символов)
>- `description`: Необязательное текстовое поле
>- `price`: Число с фиксированной точностью (10 цифр всего, 2 после запятой)
>- `duration`: Длительность в минутах (положительное целое число)
>- `is_popular`: Флаг популярности услуги

### Почему используем PositiveIntegerField вместо DurationField? ⏱️

Django предоставляет `DurationField` для хранения промежутков времени, но в нашем случае `PositiveIntegerField` (минуты) лучше по нескольким причинам:

Использование `PositiveIntegerField` вместо `DurationField` имеет несколько преимуществ: это решение проще в использовании, так как не требует преобразования в `timedelta`. Оно удобнее для расчетов, например при подсчете общей длительности услуг. Также такой формат (минуты) более понятен пользователям по сравнению с форматами типа "1:30:00".

### Подключение модели в админке 🏗️

Для управления услугами через админ-панель нужно зарегистрировать модель:

```python
from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name', 'description')
```

Такая конфигурация админки позволяет просматривать список услуг с основными полями, фильтровать их по популярности и осуществлять поиск по названию и описанию, что значительно упрощает управление услугами.

## Выстраивание связей M2M 🔗

Связи "многие-ко-многим" (Many-to-Many) в Django позволяют создавать сложные отношения между моделями. В нашем проекте такие связи используются между моделями `Master` и `Service`, а также между `Order` и `Service`.

```python
services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="masters")
```

>[!info]
>#### Особенности M2M связей
>- Один мастер может предоставлять множество услуг
>- Одна услуга может быть предоставлена множеством мастеров
>- Аналогично для заказов: один заказ может включать несколько услуг

### Как работает ManyToManyField? ⚙️

Поле `ManyToManyField` автоматически создает промежуточную таблицу в базе данных, которая хранит связи между объектами. В нашем случае Django создаст таблицы:
Django автоматически создает промежуточные таблицы `core_master_services` для связи мастеров и услуг, а также `core_order_services` для связи заказов и услуг, что обеспечивает гибкость в управлении отношениями между моделями.

Эти таблицы содержат два поля: `master_id`/`order_id` и `service_id`, образующие составной первичный ключ.

### Что такое related_name? 🔄

Параметр `related_name` определяет имя для обратной связи. Например:

```python
master = Master.objects.first()
master.services.all()  # Все услуги мастера

service = Service.objects.first()
service.masters.all()  # Все мастера, предоставляющие эту услугу (благодаря related_name="masters")
```

>[!warning]
>#### Важно о related_name
>- Если не указать `related_name`, Django использует имя по умолчанию (например, `master_set`)
>- Должен быть уникальным для каждой связи между двумя моделями

### Промежуточные модели (through) 🏗️

Если нужно хранить дополнительные данные о связи (например, цену услуги для конкретного мастера), можно создать промежуточную модель:

```python
class MasterService(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    custom_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

class Master(models.Model):
    services = models.ManyToManyField(Service, through='MasterService')
```

Теперь при добавлении связи можно указать дополнительные данные:

```python
master.services.add(service, through_defaults={'custom_price': 1500, 'notes': 'Особая цена'})
```

## Запросы к M2M 🔍

Работа со связями "многие-ко-многим" через Django ORM предоставляет мощный API для создания, чтения, обновления и удаления связей между объектами. Рассмотрим основные операции.

### Основные операции с M2M 🛠️

Django ORM предлагает удобный набор методов для управления связями "многие-ко-многим". Эти методы позволяют выполнять все основные операции с отношениями между моделями:

```python
# Добавление связей
order.services.add(service_1, service_2)  # Добавляет услуги к заказу

# Удаление связей
order.services.remove(service_1)  # Удаляет конкретную услугу

# Очистка всех связей
order.services.clear()  # Удаляет все услуги из заказа

# Замена всех связей
order.services.set([service_3, service_4])  # Заменяет текущие услуги
```

>[!info]
>#### Особенности работы с M2M
>- Методы `add()`, `remove()`, `clear()` и `set()` сразу сохраняют изменения в БД
>- Можно передавать как объекты, так и их ID
>- Для массовых операций эффективнее использовать `set()`

### Оптимизация запросов ⚡

При работе с M2M важно избегать проблемы N+1 запросов. Используйте `prefetch_related`:

```python
# Неоптимально - N+1 запросов
orders = Order.objects.all()
for order in orders:
    print(order.services.all())  # Отдельный запрос для каждого заказа

# Оптимально - 2 запроса
orders = Order.objects.prefetch_related('services').all()
for order in orders:
    print(order.services.all())  # Все услуги загружены одним запросом
```

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
