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
    
    STATUS_CHOICES = [
        ("new", "Новая"),
        ("confirmed", "Подтверждена"),
        ("completed", "Выполнена"),
        ("cancelled", "Отменена"),
    ]
    
    
    name  = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    master = models.ForeignKey(
        Master,
        verbose_name="Мастер",
        default=None,
        on_delete=models.SET_DEFAULT,
        related_name="orders",
        blank=True,
        null=True,
    )
    services = models.ManyToManyField(
        "Service", verbose_name="Услуги", related_name="orders"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        verbose_name="Статус",
        blank=True,
        null=True,
    )

    order_date = models.DateTimeField(
        verbose_name="Дата заказа", null=True, default=None
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", null=True, blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления", null=True, blank=True
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Review(models.Model):

    RATING_CHOICES = [
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    ]

    AI_CHOICES = [
        ("ai_checked_true", "Проверено ИИ"),
        ("ai_cancelled", "Отменено ИИ"),
        ("ai_checked_in_progress", "В процессе проверки"),
        ("ai_checked_false", "Не проверено"),
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

    ai_checked_status = models.CharField(
        max_length=30,
        choices=AI_CHOICES,
        default="ai_checked_false",
        verbose_name="Статус ИИ",
    )
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


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

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
