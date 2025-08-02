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
        queryset=Master.objects.none(),  # Устанавливаем пустой queryset
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Split для дата-время
    date_time = forms.SplitDateTimeField(
        label="Дата и время",
        required=True,
        widget=forms.SplitDateTimeWidget(
            date_attrs={"class": "form-control", "type": "date"},
            time_attrs={"class": "form-control", "type": "time"},
        ),
    )
    services = forms.ModelMultipleChoiceField(
        label="Услуги",
        queryset=Service.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        master_field = self.fields["master"]
        if isinstance(master_field, forms.ModelChoiceField):
            master_field.queryset = Master.objects.all()
            try:
                master_field.initial = Master.objects.get(
                    first_name__contains="Алевтина"
                )
            except (Master.DoesNotExist, Master.MultipleObjectsReturned):
                pass

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone", "")
        name = cleaned_data.get("name", "")

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

    def clean_services(self):
        master = self.cleaned_data.get("master")
        services = self.cleaned_data.get("services")

        if master and services:
            master_services = master.services.all()
            for service in services:
                if service not in master_services:
                    raise ValidationError(
                        f'Мастер {master} не предоставляет услугу "{service}".'
                    )
        return services



class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "comment", "master", "order_date", "services"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваше имя"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Телефон: +79991234567 или 89991234567",
                    "pattern": r"^(\+7|8)\d{10}$",
                }
            ),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Комментарий"}
            ),
            "master": forms.Select(attrs={"class": "form-control"}),
            # "order_date": forms.SplitDateTimeWidget(
            #     date_attrs={"class": "form-control", "type": "date"},
            #     time_attrs={"class": "form-control", "type": "time"},
            # ),

            # Пробуем обычный вариант без Split
            "order_date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "services": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        pattern = r"^(\+7|8)\d{10}$"

        if not re.match(pattern, data):
            raise ValidationError(
                "Номер телефона должен быть в формате 89123433333 или +79123433333"
            )
        return data

    def clean_services(self):
        master = self.cleaned_data.get("master")
        services = self.cleaned_data.get("services")

        if master and services:
            master_services = master.services.all()
            for service in services:
                if service not in master_services:
                    raise ValidationError(
                        f'Мастер {master} не предоставляет услугу "{service}".'
                    )
        return services




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
