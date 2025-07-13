from django.shortcuts import render, HttpResponse


def register(request):
    return HttpResponse("Регистрация")


def login(request):
    return HttpResponse("Авторизация")


def logout(request):
    return HttpResponse("Выход")
