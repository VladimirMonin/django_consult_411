from django.urls import reverse


def get_main_menu(request):
    """Функция возвращает список пунктов меню для сайта"""

    context = {
        "menu": [
            {"name": "Главная", "url": reverse("landing")},
            {"name": "О нас", "url": reverse("landing") + "#about"},
            {"name": "Преимущества", "url": reverse("landing") + "#benefits"},
            {"name": "Мастера", "url": reverse("landing") + "#masters"},
            {"name": "Услуги", "url": reverse("landing") + "#services"},
            {"name": "Запись", "url": reverse("landing") + "#booking"},
            {"name": "Управление", "url": reverse("order_list")},
        ]
    }

    return context