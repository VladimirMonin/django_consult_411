from pickle import FLOAT
from token import NAME, STRING
from django.shortcuts import render
from django.http import HttpResponse
from .data import *

# импорт функции reverse для создания URL-адресов





def landing(request):
    """Главная страница сайта - лендинг"""
    context = {
        "title": "Барбершоп - стрижки и бритье",
        "masters": masters[:3],  # Показываем только первые 3 мастера
        "services": services,
    }
    return render(request, "landing.html", context)


def order_list(request):
    context = {
        "orders": orders,
        "title": "Список заявок",
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
    }

    return render(request, "master_detail.html", context)


def master_list(request):
    context = {
        "masters": masters,
        "title": "Наши мастера",
    }
    return render(request, "master_list.html", context)

def thanks(request):
    return render(request, "thanks.html")