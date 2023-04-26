from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from . import models
from .forms import productoForm
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

now = timezone.now()

def inicio(request):
    return render (request, 'index.html')


def registrar(request):
    if request.method=='GET':
        return render (request, 'registroH.html', {'registrado': UserCreationForm})
    else:
        if len(request.POST['username'])>0 and len(request.POST['password1'])>0:
            if (request.POST['password1'] == request.POST['password2']): 
                try:
                    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('catalogo')
                except IntegrityError:
                    return render(request,'registroH.html', {'registrado': UserCreationForm, 'error': 'El usuario ya existe'})
            return render(request,'registroH.html', {'registrado': UserCreationForm, 'error': 'Las contraseñas no coinciden'})
        else:
            return render(request,'registroH.html', {'registrado': UserCreationForm, 'error': 'Ingresar usuario y contraseña'})


def ingresar(request):
    if request.method == 'GET':
        return render(request, 'ingresoH.html', {'entrada': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user == None:
            return render(request, 'ingresoH.html', {'entrada': AuthenticationForm, 'error': 'Usuario y/o contraseña incorrecto'})
        else:
            login(request, user)
            return redirect('inicio')

@login_required
def catalogoT(request):
    if request.method=='GET':
        return render(request, 'catalogoH.html', {'catalogo': productoForm})
    else:
        user = models.paciente.objects.create(
            nombre=request.POST['nombre'], 
            apellidos=request.POST['apellidos'],
            direccion=request.POST['direccion'],
            ciudad=request.POST['ciudad'],
            telefono=request.POST['telefono'],
            ingreso=now,
            alta=now,
            historial_clinico=request.POST['historial_clinico'])
        user.save()
        return render(request, 'catalogoH.html', {'catalogo': productoForm})

@login_required
def busqueda(request):
    if request.method=='GET':
        return render(request, 'buscarH.html')
    else:
        pac = models.paciente.objects.all().filter(nombre__icontains=request.POST['nombre'])
        return render(request, 'buscarH.html', {'nombres': pac})
    
@login_required
def resultado(request, elPaciente):
    pac = get_object_or_404(models.paciente, pk=elPaciente)
    return render(request, 'resultadoH.html', {'paci': pac})

def salir(request):
    logout(request)
    return redirect('inicio')