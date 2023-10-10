from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def hello(request):
    return HttpResponse("<h3>Hola mundo</h3>")


def about(request):
    return HttpResponse("<h3>ABOUT</h3>")
