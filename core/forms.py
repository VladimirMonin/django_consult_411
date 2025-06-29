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
