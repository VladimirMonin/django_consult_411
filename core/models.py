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

- `text`: TextField (verbose_name="Текст отзыва")
- `client_name`: CharField (max_length=100, blank=True, verbose_name="Имя клиента")
- `master`: ForeignKey (на мастера, on_delete=models.CASCADE, verbose_name="Мастер")
- `photo`: ImageField (upload_to="reviews/", blank=True, null=True, verbose_name="Фотография")
- `created_at`: DateTimeField (auto_now_add=True, verbose_name="Дата создания")
- `rating`: PositiveSmallIntegerField (с валидаторами MinValueValidator(1) и MaxValueValidator(5), verbose_name="Оценка") (Или через CHOICES)
- `is_published`: BooleanField (default=True, verbose_name="Опубликован")
"""


class Review(models.Model):
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
        verbose_name="Оценка", min_value=1, max_value=5
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
