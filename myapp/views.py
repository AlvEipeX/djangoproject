from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Project, Task
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CreateNewTask
from .forms import CreateNewProject

# Create your views here.


def login(request):
    return render(request, "login.html")


def home(request):
    title = "Django Course!!"
    return render(request, "index.html", {"title": title})


def about(request):
    return render(request, "about.html")


def projects(request):
    """projects = list(Project.objects.values())"""
    projects = Project.objects.all()
    return render(request, "projects.html", {"projects": projects})


def tasks(request):
    tasks = Task.objects.all()
    return render(request, "tasks.html", {"tasks": tasks})


def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": CreateNewTask()})
    else:
        Task.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            project_id=1,
        )
        return redirect("/tasks/")


def create_project(request):
    if request.method == "GET":
        return render(request, "create_project.html", {"form": CreateNewProject()})
    else:
        project = Project.objects.create(name=request.POST["name"])
        return render(request, "create_project.html", {"form": CreateNewProject()})
