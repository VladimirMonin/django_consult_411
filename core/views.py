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

def master_detail(request, master_id):
    try:
        master = [master for master in masters if master['id'] == master_id][0]

    except IndexError:
        return HttpResponse("Мастер не найден", status=404)
    
    context = {
        "master": master,
    }


    return render(request, 'master_detail.html', context)