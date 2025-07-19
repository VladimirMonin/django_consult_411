from pickle import FLOAT
from token import NAME, STRING
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .data import *

from django.db.models import Q
from .models import Order, Master, Service

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm, ReviewModelForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
import json


class LandingView(View):

    def get(self, request):
        context = {
            "title": "Барбершоп - стрижки и бритье",
            "masters": Master.objects.all()[:3],
            "services": Service.objects.all(),
        }
        return render(request, "landing.html", context)


# http://127.0.0.1:8000/orders/?q=cotiki&search_by_phone=true&search_by_name=true&search_by_comment=true&order_by_date=desc&status_new=true&status_confirmed=true&status_completed=true&status_cancelled=true
@login_required
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

class OrderListView(ListView):
    model = Order
    template_name = "order_list.html"
    context_object_name = "orders"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Заявки на стрижки"
        return context

    def get_queryset(self):
         # Получаем параметры запроса
        q = self.request.GET.get("q")

        # Чекбоксы поиска по телефону, имени и комментарию
        search_by_phone = self.request.GET.get("search_by_phone", "false") == "true"
        search_by_name = self.request.GET.get("search_by_name", "false") == "true"
        search_by_comment = self.request.GET.get("search_by_comment", "false") == "true"

        # Радиокнопки направления сорртировки по дате
        order_by_date = self.request.GET.get("order_by_date", "desc")

        # Чекбоксы статусов заказов
        status_new = self.request.GET.get("status_new", "false") == "true"
        status_confirmed = self.request.GET.get("status_confirmed", "false") == "true"
        status_completed = self.request.GET.get("status_completed", "false") == "true"
        status_cancelled = self.request.GET.get("status_cancelled", "false") == "true"

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

        return query
            




class MasterDetailView(DetailView):
    model = Master
    template_name = "master_detail.html"
    pk_url_kwarg = "master_id"

class MasterListView(ListView):
    model = Master
    template_name = "master_list.html"
    context_object_name = "masters"
    ordering = ["-name"]

    def get_queryset(self):
        # Определим мастеров у которых есть хотя бы одна услуга
        masters = Master.objects.prefetch_related("services").filter(
            services__isnull=False
        ).distinct()
        return masters

class ThanksTemplateView(TemplateView):
    template_name = "thanks.html"


def review_create(request):
    if request.method == "GET":
        form = ReviewModelForm()
        context = {
            "title": "Оставить отзыв",
            "button_text": "Отправить отзыв",
            "form": form,
        }
        return render(request, "review_form.html", context)

    elif request.method == "POST":
        form = ReviewModelForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "title": "Оставить отзыв",
                "button_text": "Отправить отзыв",
                "form": form,
            }
            # Отправка сообщения об ошибке
            messages.error(request, "Форма заполнена некорректно")
            return render(request, "review_form.html", context)

        form.save()
        # Отправка сообщения об успешной отправке
        messages.success(request, "Отзыв успешно отправлен")
        return redirect("thanks")


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
            order_date=form.cleaned_data["date_time"],
        )

        # Множественно установим связи M2M для услуг
        order.services.set(form.cleaned_data["services"])

        # Редирект на страницу благодарности
        return redirect("thanks")


class MasterServicesView(View):

    # def dispatch(self, request, *args, **kwargs):
    #     """
    #     Возвращаем ошибку если метод не POST
    #     Это избыточно. Классовая вью и без этого вернет 405
    #     """
    #     if request.method != "POST":
    #         return JsonResponse({"error": "Иди отдыхай"}, status=405)

    def post(self, request, master_id):
        try:
            data = json.loads(request.body)
            master_id = data.get("master_id")
            master = Master.objects.get(id=master_id)
            services = master.services.all()
            services_data = [
                {"id": service.id, "name": service.name} for service in services
            ]
            return JsonResponse({"services": services_data})
        except Master.DoesNotExist:
            return JsonResponse({"error": "Master not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


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
                "date_time": order.order_date,
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
        order.order_date = form.cleaned_data["date_time"]
        order.services.set(form.cleaned_data["services"])
        order.save()

        # Редирект на страницу благодарности
        return redirect("thanks")
