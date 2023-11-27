from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Project, Task
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CreateNewTask

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


def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'tasks.html', {
        'tasks': tasks
    })


def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {
            'form': CreateNewTask()
        })
    else:
        Task.objects.create(
            title=request.POST['title'], description=request.POST['description'], project_id=1)
        return redirect('/tasks/')


def hello(request, username):
    return HttpResponse(
        "<h3>Hello %s</h3>" % username
    )
