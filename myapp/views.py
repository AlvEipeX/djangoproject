from .forms import TaskForm
from .models import UsuarioPersonalizado, diario, Task
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from datetime import datetime
from datetime import time
from django.db import IntegrityError
import pandas as pd
from django.http import HttpResponse

# Create your views here.


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        print(request.POST)
        try:
            if request.POST["is_superuser"] == "on":
                superusuario = True
        except:
            superusuario = False
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = UsuarioPersonalizado.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                    first_name=request.POST["first_name"],
                    last_name=request.POST["last_name"],
                    email=request.POST["email"],
                    fec_nac=request.POST["fec_nac"],
                    salario=request.POST["salario"],
                    is_superuser=superusuario,
                )
                user.save()
                login(request, user)
                return redirect("signin")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Usuario ya registrado"},
                )
            except ValueError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Datos no validos"},
                )
            except:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Error en el registro"},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Los Passwords no coinciden"},
        )


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            print(request.POST["username"])
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Usuario o Password incorrecto(s)",
                },
            )
        else:
            login(request, user)
            if user.is_superuser == True:
                return redirect("control")
            else:
                return redirect("marcar")


def about(request):
    return render(request, "about.html")


@login_required
def control(request):
    usuario = request.user
    empleados = UsuarioPersonalizado.objects.filter(is_superuser=False)
    return render(request, "control.html", {"usuario": usuario, "empleados": empleados})


@login_required
def marcar(request):
    ahora = datetime.now()
    usuario = request.user
    return render(request, "marcar.html", {"usuario": usuario, "fec_hora": ahora})


@login_required
def marcar_llegada(request):
    fecha_actual = timezone.now().date()
    hora_actual = datetime.now().time()
    hora_format = hora_actual.strftime("%H:%M:%S")
    ahora = datetime.now()
    usuario = request.user
    verificacion = diario.objects.filter(fech_reg=fecha_actual, empleado=usuario.id)
    if verificacion.exists():
        print("Ya existe")
    else:
        print("No existe")

    if time(5, 0, 0) <= hora_actual <= time(8, 10, 0):
        tiempo_retraso = False
        mensaje = (
            "Bienvenido \nHora registrada de ingreso: "
            + str(hora_format)
            + "\nLlegada registrada correctamente"
        )
    else:
        tiempo_retraso = True
        mensaje = (
            "Bienvenido empleado \n\n Su hora registrada de ingreso es: "
            + str(hora_format)
            + "\n\nTiempo con retraso registrado"
        )
    registro = diario(
        fech_reg=fecha_actual,
        hora_in=hora_actual,
        hora_out="00:00:00",
        retraso=tiempo_retraso,
        salida=False,
        empleado_id=usuario.id,
    )

    registro.save()
    return render(
        request,
        "marcar.html",
        {"usuario": usuario, "fec_hora": ahora, "mensaje": mensaje},
    )


@login_required
def signout(request):
    logout(request)
    return redirect("signin")


@login_required
def exportar_excel(request):
    registros = UsuarioPersonalizado.objects.filter(is_superuser=False)

    data = {
        "id": [],
        "first_name": [],
        "last_name": [],
        "email": [],
        "fec_nac": [],
        "salario": [],
    }
    for registro in registros:
        data["id"].append(registro.id)
        data["first_name"].append(registro.first_name)
        data["last_name"].append(registro.last_name)
        data["email"].append(registro.email)
        data["fec_nac"].append(registro.fec_nac)
        data["salario"].append(registro.salario)

    df = pd.DataFrame(data)
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="registros.xlsx"'
    df.to_excel(response, index=False, engine="openpyxl")

    return response


""" ------------------------------------------------------------------ """


@login_required
def tasks(request):
    usuario = request.user
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {"tasks": tasks, "usuario": usuario})


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by("-datecompleted")
    return render(request, "tasks.html", {"tasks": tasks})


@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {"form": form, "error": "No se pudo actualizar"},
            )


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "create_task.html",
                {"form": TaskForm, "error": "Datos no validos"},
            )
