from django.shortcuts import render,redirect
from .models import *


def agendamento(request,empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)

    return render(request, 'comun/agendamento.html', {'empresa': empresa})

