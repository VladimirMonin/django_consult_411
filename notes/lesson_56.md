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

## 


====================================================================
Урок 56 (3 ч): Many-to-Many, расширение модели

Новые сущности

Service, поля: name, price, duration

Master.services  – M2M

Order.services   – M2M blank=True

Цели

• Проектировать и мигрировать M2M

• Управлять связями add/remove/set/clear

• Фильтровать по M2M, проверять «мастер оказывает услугу»

Структура

00-15  Актуализация, ответы по ДЗ

15-40  Теория 1: ManyToManyField, through, blank, null

40-75  Практика 1: создать Service + M2M поля, миграции, admin

75-90  Перерыв

90-110 Теория 2: M2M API, through-model анонс

110-140 Практика 2: shell_plus — выборки, массовое add; доработка шаблона landing с prefetch_related

140-155 Теория 3: Order.services blank=True, валидация «мастер ↔ услуга»

155-175 Практика 3: функция master_provides_service, метод provides() в модели


Доп. рекомендации преподавателю

• Live-coding в shell_plus, команды в чат

• Демонстрировать on_delete различия

• При наличии – показать Django-Debug-Toolbar

• Админка: filter_horizontal для M2M


