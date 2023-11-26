from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Project, Task
from django.shortcuts import get_object_or_404, render

# Create your views here.


def home(request):
    title = 'Django Course!!'
    return render(request, 'index.html', {
        'title': title
    })


def about(request):
    username = 'al'
    return render(request, 'about.html', {
        'username': username
    })


def projects(request):
    """ projects = list(Project.objects.values()) """
    projects = Project.objects.all()
    return render(request, 'projects.html', {
        'projects': projects
    })


def tasks(request, id):
    task = get_object_or_404(Task, id=id)
    return HttpResponse('task = %s' % task.title)


def hello(request, username):
    return HttpResponse(
        "<h3>Hello %s</h3>" % username
    )
