from .forms import CreateNewTask
from .forms import CreateNewProject
from .models import Project, Task
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError

# Create your views here.


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Usuario ya existe"},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Pass not match"},
        )


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


def logout(request):
    return render(request, "logout.html")


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
