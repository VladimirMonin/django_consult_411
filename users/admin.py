from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Кастомизация админки для пользователей.
    Используем UserAdmin как основу для сохранения всего функционала
    стандартной админки пользователей (смена пароля и т.д.).
    """
    model = CustomUser

    # Добавляем наши кастомные поля в fieldsets,
    # чтобы их можно было редактировать на странице пользователя.
    # Мы добавляем новую секцию 'Дополнительная информация'.
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('avatar', 'tg_id', 'vk_id')}),
    )

    # Добавляем поля на страницу создания нового пользователя.
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('avatar', 'tg_id', 'vk_id', 'first_name', 'last_name', 'email')}),
    )

    # Определяем поля, которые будут отображаться в списке пользователей.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    # Добавляем поля для поиска.
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Добавляем фильтры.
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Указываем кликабельные поля.
    list_display_links = ('username', 'email')


# Регистрируем нашу модель с кастомным классом админки.
admin.site.register(CustomUser, CustomUserAdmin)