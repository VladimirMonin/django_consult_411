from pickle import FLOAT
from token import NAME, STRING
from django.shortcuts import render
from django.http import HttpResponse
from .data import *


def get_main_menu():
    """Функция возвращает список пунктов меню для сайта"""
    return [
        {"name": "Главная", "url": "/"},
        {"name": "О нас", "url": "#about"},
        {"name": "Преимущества", "url": "#benefits"},
        {"name": "Мастера", "url": "#masters"},
        {"name": "Услуги", "url": "#services"},
        {"name": "Запись", "url": "#booking"},
        {"name": "Управление", "url": "/orders/"},
    ]


def landing(request):
    """Главная страница сайта - лендинг"""
    context = {
        "title": "Барбершоп - стрижки и бритье",
        "menu": get_main_menu(),
        "masters": masters[:3],  # Показываем только первые 3 мастера
        "services": services,
    }
    return render(request, "landing.html", context)


def order_list(request):
    context = {
        "orders": orders,
        "title": "Список заявок",
        "menu": get_main_menu(),
    }
    return render(request, "order_list.html", context)


def index(request):
    # Перенаправляем на лендинг
    return landing(request)


def master_detail(request, master_id):
    try:
        master = [master for master in masters if master["id"] == master_id][0]

    except IndexError:
        return HttpResponse("Мастер не найден", status=404)

    context = {
        "master": master,
        "title": f"Мастер {master['name']}",
        "menu": get_main_menu(),
    }

    return render(request, "master_detail.html", context)


def master_list(request):
    context = {
        "masters": masters,
        "title": "Наши мастера",
        "menu": get_main_menu(),
    }
    return render(request, "master_list.html", context)
