from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.d


def hello(request):
    return HttpResponse("<h3>Hola s</h3>")


def about(request):
    return HttpResponse("<h3>ABOUcambio</h3>")
