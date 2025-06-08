from django.db import models


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


class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    master = models.ForeignKey(Master, verbose_name="Мастер", default=None, on_delete=models.SET_DEFAULT)


# Простая выборка в shell plus
# orders = Order.objects.all() - получаем QuerySet всех объектов - это служебная коллекция
# Если попростить orders[0] - Мы получаем из коллекции экземпляр Order
# orders[0].name - Фродо. Получили данные из поля
# orders[0].master.first_name - Получаем данные из связанной модели