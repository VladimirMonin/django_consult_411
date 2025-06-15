from django.contrib import admin
from .models import Master, Order, Review, Service


# Сделать регистрацию самым простым способом
admin.site.register(Master)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Service)

