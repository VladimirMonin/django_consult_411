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

"""
**Review (Отзыв)**

Модель для хранения отзывов клиентов о мастерах.

Поля:
- `text`: TextField (verbose_name="Текст отзыва") - Содержание отзыва.
- `client_name`: CharField (max_length=100, blank=True, null=True, verbose_name="Имя клиента") - Имя клиента, оставившего отзыв. Может быть пустым.
- `master`: ForeignKey (Master, on_delete=models.SET_NULL, null=True, verbose_name="Мастер") - Ссылка на мастера, которому оставлен отзыв. Если мастер удален, поле становится NULL.
- `photo`: ImageField (upload_to="reviews/", blank=True, null=True, verbose_name="Фотография") - Фотография, прикрепленная к отзыву. Может быть пустой.
- `created_at`: DateTimeField (auto_now_add=True, verbose_name="Дата создания") - Дата и время создания отзыва. Устанавливается автоматически при создании.
- `rating`: PositiveSmallIntegerField (verbose_name="Оценка", choices=RATING_CHOICES, default=5) - Оценка отзыва по шкале от 1 до 5.
- `is_published`: BooleanField (default=False, verbose_name="Опубликован") - Флаг, указывающий, опубликован ли отзыв.

RATING_CHOICES:
- 1: "Ужасно"
- 2: "Плохо"
- 3: "Нормально"
- 4: "Хорошо"
- 5: "Отлично"
"""


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


"""
**Service (Услуга)**

- `name`: CharField (max_length=200, verbose_name="Название")
- `description`: TextField (blank=True, verbose_name="Описание")
- `price`: DecimalField (max_digits=10, decimal_places=2, verbose_name="Цена")
- `duration`: PositiveIntegerField (verbose_name="Длительность", help_text="Время выполнения в минутах")
- `is_popular`: BooleanField (default=False, verbose_name="Популярная услуга")
- `image`: ImageField (upload_to="services/", blank=True, verbose_name="Изображение")
"""


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(
        verbose_name="Длительность", help_text="Время выполнения в минутах", default=20
    )
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
