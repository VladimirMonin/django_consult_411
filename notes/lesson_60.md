# Тема Django Forms Ч2. Урок 60

## Формы Django

- Какие задачи решают фомры в Django?
- Типы форм в Django
- Создание формы

## Таблица типов полей и их валидаторов

- Сделать большую таблицу с типами полей и валидаторами которые у них есть (чтобы было описание)
- Расскажи про Widjets - какие они бываают
- Какие еще свойства у полей есть? label, queryset, required, widget, initial и...

```python
# ./core/forms.py
from django import forms
from .models import Order, Service, Review, Master
from django.core.exceptions import ValidationError


# Форма не связанная с моделью
class OrderForm(forms.Form):
    name = forms.CharField(label="",max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}))
    phone = forms.CharField(label="",max_length=20, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваш телефон"}))
    comment = forms.CharField(label="",required=False, widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Комментарий"}))
    master = forms.ModelChoiceField(
        label="Мастер", 
        queryset=Master.objects.all(), 
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        initial = Master.objects.get(first_name__contains="Алевтина")
    )
    services = forms.ModelMultipleChoiceField(
        label="Услуги",
        queryset=Service.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )
```

- Изменение шаблона

```html
{% extends "base.html" %}
{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card mt-5">
                <div class="card-body text-center">
                    <h1 class="card-title">
                        {{ title }}
                    </h1>
                    <form action="" method="post">
                        {% csrf_token %}
                       {{ form.as_p }}
                        <button type="submit" class="btn btn-dark">{{ button_text }}</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

Как видите у нас все стало проще в шаблоне. Просто рендерим форму через `{{ form.as_p }}`

- Изменение View Для создания и обновления записи

```python
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
```

- Как работают эти вью?
- Что такое `is_valid()`?
- Что происходит при вызове `form.is_valid()`?
- Что такое `cleaned_data`?
- Когда и как формируются данные в `cleaned_data`?

## Методы `clean()` и `clean_<field_name>()`

```python
# ./core/forms.py
from django import forms
from .models import Order, Service, Review, Master
from django.core.exceptions import ValidationError
import re


# Форма не связанная с моделью
class OrderForm(forms.Form):
    name = forms.CharField(
        label="",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ваше имя"}
        ),
    )
    phone = forms.CharField(
        label="",
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Телефон: +79991234567 или 89991234567",
                "pattern": r"^(\+7|8)\d{10}$",

            }
        ),
    )
    comment = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Комментарий"}
        ),
    )
    master = forms.ModelChoiceField(
        label="Мастер",
        queryset=Master.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        initial=Master.objects.get(first_name__contains="Алевтина"),
    )
    services = forms.ModelMultipleChoiceField(
        label="Услуги",
        queryset=Service.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone", '')
        name = cleaned_data.get("name", '')

        if len(phone) + len(name) < 14:
            raise ValidationError("Имя + телефон должны быть не менее 14 символов")

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        pattern = r"^(\+7|8)\d{10}$"

        if not re.match(pattern, data):
            raise ValidationError(
                "Номер телефона должен быть в формате 89123433333 или +79123433333"
            )

        return data
```

- Что такое `clean()`?
- Что такое `clean_<field_name>()`?
- Когда отрабатывают эти методы?
- Какие вещи можно делать в `clean()`?

## ModelForm

- Что такое `ModelForm`?
- Чем она отличается от обычных форм?
- Как создать `ModelForm`?

```python
# Форма связанная с моделью
class ReviewModelForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["client_name", "text", "master", "photo", "rating"]
        widgets = {
            "client_name": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "master": forms.Select(attrs={"class": "form-control"}),
            "rating": forms.Select(attrs={"class": "form-control"}),
        }
```

- Поясненя как работает эта форма
- Что класс `Meta` есть только у `ModelForm`
- Что в него можно вписать
- Что все валидаторы берутся из полей модели
- Что все связанные данные берутся из полей модели
- Что такое `fields`?
