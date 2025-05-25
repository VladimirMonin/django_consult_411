from pickle import FLOAT
from token import NAME, STRING
from django.shortcuts import render
from django.http import HttpResponse
from .data import *



def index(request):
    context = {
        "name": "Арбуз",
    }
    return render(request, 'first_template.html', context)
