from pickle import FLOAT
from token import NAME, STRING
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .data import *

from django.db.models import Q
from .models import Order, Master, Service, Review

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm, ReviewModelForm, OrderModelForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import json

# Импорт LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin


from django.urls import reverse, reverse_lazy

# Собственный класс проверяем юзер из став и юзер из админ

class AdminStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_active


class LandingView(View):

    def get(self, request):
        context = {
            "title": "Барбершоп - стрижки и бритье",
            "masters": Master.objects.all()[:3],
            "services": Service.objects.all(),
        }
        return render(request, "landing.html", context)



class OrderListView(LoginRequiredMixin, ListView):
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
 

class ReviewCreateView(CreateView):
    # model = Review
    form_class = ReviewModelForm
    template_name = "review_form.html"
    success_url = reverse_lazy("thanks")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оставить отзыв"
        context["button_text"] = "Отправить отзыв"
        return context
    
    def form_valid(self, form):
        # Отправляем сообщение об успешной отправке
        messages.success(self.request, "Отзыв успешно отправлен")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Отправляем сообщение об ошибке
        messages.error(self.request, "Форма заполнена некорректно")
        return super().form_invalid(form)


class MasterServicesView(View):

    # def dispatch(self, request, *args, **kwargs):
    #     """
    #     Возвращаем ошибку если метод не POST
    #     Это избыточно. Классовая вью и без этого вернет 405
    #     """
    #     if request.method != "POST":
    #         return JsonResponse({"error": "Иди отдыхай"}, status=405)

    def post(self, request):
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



class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    model = Order
    form_class = OrderModelForm
    template_name = "order_form_class.html"
    success_url = reverse_lazy("order_list")
    pk_url_kwarg = "order_id"
    permission_required = "core.change_order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование заявки"
        context["button_text"] = "Сохранить"
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Заявка успешно обновлена")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Форма заполнена некорректно")
        return super().form_invalid(form)
    

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderModelForm
    template_name = "order_form_class.html"
    success_url = reverse_lazy("order_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создание заявки"
        context["button_text"] = "Сохранить"
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Заявка успешно создана")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Форма заполнена некорректно")
        return super().form_invalid(form)