from django.contrib import admin
from .models import Master, Order


# Сделать регистрацию самым простым способом
admin.site.register(Master)
admin.site.register(Order)

