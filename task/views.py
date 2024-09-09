from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from django.utils import timezone
from .models import Task
from .forms import TaskFormCreate

import datetime


# Create your views here.
def home(request):
    dtime = datetime.datetime.now()
    return render(request, 'home.html', {
        'user': request.user,
        'hour': dtime.hour
    })


def registration(request):
    return render(request, 'registration.html', {
        'form': UserCreationForm
    })


def sign_up(request):
    if request.method == "GET":
        print("Enviando datos")
        return render(request, 'sign_up.html', {
            'form': UserCreationForm
        })
    else:
        equals = False
        if request.POST["password1"] == request.POST["password2"]:
            equals = True
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'sign_up.html', {
                    'form': UserCreationForm,
                    'error': "Username already exists"
                })
        else:
            equals = False
            return render(request, 'registration.html', {
                "equals": equals,
                "error": "None"
            })


@login_required()
def tasks(request):
    return render(request, 'task/tasks.html', {
        "tasks": Task.objects.filter(user=request.user, datecompleted__isnull=True)
    })


@login_required()
def tasks_completed(request):
    tasks = Task.objects.filter(
        user_id=request.user.id, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'task/tasks.html', {
        "tasks": tasks
    })


@login_required()
def create_task(request):
    if request.method == "GET":
        return render(request, 'task/create_task.html', {
            "form": TaskFormCreate
        })
    else:
        form = TaskFormCreate(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            try:
                new_task.save()
                return redirect("tasks")
            except ValueError:
                form.add_error(None, "Error al guardar los cambios")
        form.add_error(None, "Completa los campos")
        return render(request, 'task/create_task.html', {
            "form": form
        })


@login_required()
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user_id=request.user.id)
    form = TaskFormCreate(instance=task)

    if request.method == 'GET':
        return render(request, 'task/task_detail.html', {
            "task": task,
            "form": form
        })
    else:
        form = TaskFormCreate(request.POST, instance=task)
        if form.is_valid():
            # Hacer la actualizacion del objeto
            try:
                form.save()
                return redirect('tasks')
            except IntegrityError as e:
                form.add_error(None, f"Error al actualizar la tarea: {e}")
        return render(request, 'task/task_detail.html', {
            "task": task,
            "form": form
        })


@login_required()
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskFormCreate(instance=task)
    if request.method == 'POST':
        try:
            task.datecompleted = timezone.now()
            task.save()
            return redirect('tasks')
        except IntegrityError as e:
            form.add_error(None, f"Error al completar la tarea: {e}")
            return render(request, 'task/task_detail.html', {
                "task": task,
                "form": form
            })


@login_required()
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskFormCreate(instance=Task)
    if request.method == 'POST':
        try:
            task.delete()
            return redirect('tasks')
        except IntegrityError as e:
            form.add_error(None, f"Error al eliminar la tarea: {e}")
            return render(request, 'task/task_detail.html', {
                "task": task,
                "form": form
            })


@login_required()
def log_out(request):
    logout(request)
    # return render(request, 'log_out.html')
    return redirect('home')


def sign_in(request):
    form = None
    if request.method == "GET":
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user_name_f = form.cleaned_data.get("username")
            password_f = form.cleaned_data.get("password")
            user = authenticate(
                request, username=user_name_f, password=password_f)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Usuario o contraseña incorrectos")
        else:
            form.add_error(None, "Corrige los errores")
    return render(request, 'sign_in.html', {
        "form": form
    })
