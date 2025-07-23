from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import MovimientoForm
from .models import Movimiento, Categoria

# Create your views here.
@login_required
def home(request):
    categorias = Categoria.objects.all()
    movimientos = Movimiento.objects.filter(usuario=request.user).order_by('-fecha')
    ingresos = 0
    gastos = 0
    for movimiento in movimientos:
        if movimiento.tipo == 'ingreso':
            ingresos += movimiento.monto
        if movimiento.tipo == 'gasto':
            gastos += movimiento.monto
    
    diferencia = ingresos - gastos
    
    if request.method == 'GET':
        return render(request, 'home.html', {
            'movimientos': movimientos,
            'filtro_tipo': 'todos',
            'filtro_categoria': 'todas',
            'categorias': categorias,
            'ingresos': ingresos,
            'gastos': gastos,
            'diferencia': diferencia,
            'usuario': request.user
        })
    else:
        filtro_tipo = request.POST.get('filtro', 'todos')
        filtro_categoria = request.POST.get('filtro_categoria', 'todas')
        if filtro_tipo != 'todos':
            movimientos = movimientos.filter(usuario=request.user, tipo=filtro_tipo)
        if filtro_categoria != 'todas':
            movimientos = movimientos.filter(usuario=request.user, categoria__id=filtro_categoria)

        return render(request, 'home.html', {
            'movimientos': movimientos,
            'filtro_tipo': filtro_tipo,
            'filtro_categoria': filtro_categoria,
            'categorias': categorias,
            'ingresos': ingresos,
            'gastos': gastos,
            'usuario': request.user
        })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'error': 'Credenciales Incorrectas',
                'form': AuthenticationForm
            })
        else:
            login(request, user)
            return redirect('home')

def signup(request): 
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #Registrar usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })
    
@login_required
def signout(request):
    logout(request)
    return redirect('login')

@login_required
def crear_movimiento(request):
    if request.method == 'GET':
        return render(request, 'crear_movimiento.html', {
            'form': MovimientoForm
        })
    else:
        try:
            form = MovimientoForm(request.POST)
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.save()
            return redirect('home')
        except:
            return render(request, 'crear_movimiento.html', {
            'form': MovimientoForm,
            'error': 'Ingrese datos validos'
        })

@login_required
def borrar_movimiento(request, id):
    movimiento = get_object_or_404(Movimiento, pk=id, usuario=request.user)
    movimiento.delete()
    return redirect('home')

@login_required
def editar_movimiento(request, id):
    if request.method == 'GET':
        movimiento = get_object_or_404(Movimiento, pk=id, usuario=request.user)
        form = MovimientoForm(instance=movimiento)
        return render(request, 'editar_movimiento.html', {
            'form': form
        })
    else:
        try:
            movimiento = get_object_or_404(Movimiento, pk=id, usuario=request.user)
            form = MovimientoForm(request.POST, instance=movimiento)
            form.save()
            return redirect('home') 
        except:
                return render(request, 'editar_movimiento.html', {
                'form': MovimientoForm,
                'error': 'Ingrese datos validos'
            })