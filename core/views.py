from pickle import FLOAT
from token import STRING
from django.shortcuts import render
from django.http import HttpResponse

# Представление главной страницы
class Name:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def age_in_days(self):
        return self.age * 365

    def __str__(self):
        return f'Метод __str__ класса Name: {self.name}'


INTEGER = 1
FLOAT = 1.0
STRING = "1"
NUM_LIST = [1, 2, 3]
NAME_DICT = {
    "name": "Арбуз",
    "price": 100,
    "is_ripe": True,
    "weight": 1.5,
    "colors": ["red", "green", "yellow"],
}
STRING_SET = {"red", "green", "yellow"}

#PRACTICE Эсперимент с типами данных в шаблоне
"""
1. Передать все в контекст шаблона
2. Описать в шаблоне типы данных
3. Попробовать вывести в шаблоне элемент списка по индексу через [0]
4. Попробовать вывести через .
5. Попробовать обратится через точку к атрибуту класса
6. Попробовать через точку обратится к ключу словаря
7. Попробовать через точку вызывать метод класса
"""


def index(request):
    context = {
        "name": "Арбуз",
        "integer": INTEGER,
    }
    return render(request, 'first_template.html', context)
