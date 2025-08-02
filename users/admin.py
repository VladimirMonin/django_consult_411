from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Временно регистрируем модель со стандартным UserAdmin для отладки.
# Это поможет проверить, вызвана ли ошибка кастомными настройками.
admin.site.register(CustomUser, UserAdmin)