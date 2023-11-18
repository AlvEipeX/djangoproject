from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Project, Task
from django.shortcuts import get_object_or_404

# Create your views here.a


def about(request):
    return HttpResponse("<h3>ABOUcambio</h3>")


def projects(request):
    projects = list(Project.objects.values())
    return JsonResponse(projects, safe=False)


def tasks(request, id):
    task = get_object_or_404(Task, id=id)
    return HttpResponse('task = %s' % task.title)


def home(request):
    return HttpResponse("<h3>CASA</h3>")


def hello(request, username):
    return HttpResponse(
        "<h3>Hello %s</h3>" % username
    )
