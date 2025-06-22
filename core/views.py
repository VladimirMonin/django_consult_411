from pickle import FLOAT
from token import NAME, STRING
from django.shortcuts import render
from django.http import HttpResponse
from .data import *

from django.db.models import Q
from .models import Order

# импорт функции reverse для создания URL-адресов





def landing(request):
    """Главная страница сайта - лендинг"""
    context = {
        "title": "Барбершоп - стрижки и бритье",
        "masters": masters[:3],  # Показываем только первые 3 мастера
        "services": services,
    }
    return render(request, "landing.html", context)

#http://127.0.0.1:8000/orders/?q=cotiki&search_by_phone=true&search_by_name=true&search_by_comment=true&order_by_date=desc&status_new=true&status_confirmed=true&status_completed=true&status_cancelled=true
def order_list(request):
    
    # Получаем параметры запроса
    q = request.GET.get("q")

    # Чекбоксы поиска по телефону, имени и комментарию
    search_by_phone = request.GET.get("search_by_phone", "false") == "true"
    search_by_name = request.GET.get("search_by_name", "false") == "true"
    search_by_comment = request.GET.get("search_by_comment", "false") == "true"
    
    # Радиокнопки направления сорртировки по дате
    order_by_date = request.GET.get("order_by_date", "desc")
    
    # Чекбоксы статусов заказов
    status_new = request.GET.get("status_new", "false") == "true"
    status_confirmed = request.GET.get("status_confirmed", "false") == "true"
    status_completed = request.GET.get("status_completed", "false") == "true"
    status_cancelled = request.GET.get("status_cancelled", "false") == "true"

    # Cоздаем базовый запрос
    query = Order.objects.all()

    # Создаем базовую Q
    base_q = Q()

    # Серия IF где мы модифицируем базовый запрос в зависимости от чекбоксов и радиокнопок

    # Представим, что в Order у нас есть поле status формата choises с следующими значениями:
    # new, confirmed, completed, cancelled
    if q:
        if search_by_phone:
            base_q |= Q(phone__icontains=q)
        
        if search_by_name:
            base_q |= Q(name__icontains=q)
        
        if search_by_comment:
            base_q |= Q(comment__icontains=q)
    
    # Ветвление по радиокнопкам направления сортировки по дате
    if order_by_date == "asc":
        query = query.order_by("date")
    else:
        query = query.order_by("-date")
    
    # Ветвление по чекбоксам статуса заявок
    if status_new:
        base_q &= Q(status="new")

    if status_confirmed:
        base_q &= Q(status="confirmed")

    if status_completed:
        base_q &= Q(status="completed")

    if status_cancelled:
        base_q &= Q(status="cancelled")


    # Объединяем базовый запрос и базовую Q
    query = query.filter(base_q)

    context = {
        "orders": query,
        "title": "Заявки на стрижки",
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

def order_create(request):
    return render(request, "order_form.html")