from django.shortcuts import render
from django.http import HttpResponse

# Представление главной страницы


def index(request):
    return HttpResponse('<h1>Приветствуем в барбершопе "Арбуз"!!!</h1>')
