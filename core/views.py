from django.shortcuts import render
from django.http import HttpResponse

# Представление главной страницы


def index(request):
    context = {
        "name": "Арбуз"
    }
    return render(request, 'first_template.html', context)
