from pickle import FLOAT
from token import NAME, STRING
from django.shortcuts import render
from django.http import HttpResponse
from .data import *

from django.db.models import Q
from .models import Order

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm


def landing(request):
    """Главная страница сайта - лендинг"""
    context = {
        "title": "Барбершоп - стрижки и бритье",
        "masters": masters[:3],  # Показываем только первые 3 мастера
        "services": services,
    }
    return render(request, "landing.html", context)


# http://127.0.0.1:8000/orders/?q=cotiki&search_by_phone=true&search_by_name=true&search_by_comment=true&order_by_date=desc&status_new=true&status_confirmed=true&status_completed=true&status_cancelled=true
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
        query = query.order_by("created_at")
    else:
        query = query.order_by("-created_at")

    # Ветвление по чекбоксам статуса заявок
    if status_new:
        base_q |= Q(status="new")

    if status_confirmed:
        base_q |= Q(status="confirmed")

    if status_completed:
        base_q |= Q(status="completed")

    if status_cancelled:
        base_q |= Q(status="cancelled")

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
    if request.method == "GET":
        form = OrderForm()
        # Контекст для передачи в шаблон
        context = {
            "title": "Заявка на стрижку",
            "button_text": "Записаться",
            "form": form,
        }
        return render(request, "order_form_class.html", context)

    elif request.method == "POST":
        # Валидация формы
        form = OrderForm(request.POST)

        # Если форма НЕ валидна, то возвращаем форму с ошибками
        if not form.is_valid():
            context = {
                "title": "Заявка на стрижку",
                "button_text": "Записаться",
                "form": form,
            }
            return render(request, "order_form_class.html", context)

        # Создаем объект заявки
        order = Order.objects.create(
            name=form.cleaned_data["name"],
            phone=form.cleaned_data["phone"],
            comment=form.cleaned_data["comment"],
            master=form.cleaned_data["master"],
        )

        # Множественно установим связи M2M для услуг
        order.services.set(form.cleaned_data["services"])

        # Редирект на страницу благодарности
        return redirect("thanks")


def order_update(request, order_id):
    if request.method == "GET":
        # Получаем объект заявки
        try:
            order = Order.objects.get(id=order_id)
        except ObjectDoesNotExist:
            return HttpResponse("Заявка не найдена", status=404)

        # Создаем форму и передаем в нее данные из объекта заявки
        form = OrderForm(
            initial={
                "name": order.name,
                "phone": order.phone,
                "comment": order.comment,
                "master": order.master,
                "services": order.services.all(),
            }
        )

        context = {
            "title": "Редактирование заявки",
            "button_text": "Сохранить",
            "order": order,
            "form": form,
        }
        return render(request, "order_form_class.html", context)

    elif request.method == "POST":
        # Валидация формы
        form = OrderForm(request.POST)

        # Если форма НЕ валидна, то возвращаем форму с ошибками
        if not form.is_valid():
            context = {
                "title": "Редактирование заявки",
                "button_text": "Сохранить",
                "form": form,
            }

            return render(request, "order_form_class.html", context)

        # Обновляем данные объекта заявки
        order = Order.objects.get(id=order_id)
        order.name = form.cleaned_data["name"]
        order.phone = form.cleaned_data["phone"]
        order.comment = form.cleaned_data["comment"]
        order.master = form.cleaned_data["master"]
        order.services.set(form.cleaned_data["services"])
        order.save()

        # Редирект на страницу благодарности
        return redirect("thanks")
