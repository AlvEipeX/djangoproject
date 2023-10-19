from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.dadsSa


def hello(request, username):
    return HttpResponse(
        "<h3>Hello %s</h3>" % username
    )


def about(request):
    return HttpResponse("<h3>ABOUcambio</h3>")
