# Control de Gastos – Django

Una aplicación web sencilla para registrar, categorizar y visualizar tus gastos personales, construida con Django.

## 🏗️ Tecnologías

- **Backend**: Python 3.x, Django
- **Base de Datos**: SQLite (puede cambiarse a PostgreSQL, MySQL, etc.)
- **Frontend**: Django Templates + Bootstrap
- **Autenticación**: Sistema de usuarios integrado con Django

---

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/DenzelRdz/control-de-gastos-django.git
   cd control-de-gastos-django
2. Crea y activa un entorno virtual
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux/macOS
   .venv\Scripts\activate
3. Instala dependencias
   ```bash
   pip install -r requirements.txt
4. Aplica las migraciones
   ```bash
   python manage.py migrate
5. Crea un superusuario (opcional)
   ```bash
   python manage.py createsuperuser
6. Ejecuta el servidor
   ```bash
   python manage.py runserver

Accede en tu navegador a http://127.0.0.1:8000/

---

## 🎯 Funcionalidades
- Registro de Ingresos y Gastos
- Categorías personalizables
- Vista general del historial de movimientos
- Filtrado por tipo y categoría
- Resumen total de ingresos, gastos y diferencia

---

## 📂 Estructura del Proyecto

```
control_de_gastos/               
├── settings.py           # Configuración principal
├── urls.py
└── wsgi.py
├── finanzas/               # Aplicación principal
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---
## Modelos

### Categoría
```python
class Categoria(models.Model):
   nombre = models.CharField(max_length=50)
   def __str__(self):
      return self.nombre
```
- El modelo de categoría cuenta con el atributo de nombre y una función str para visualizarlo mejor en el administrador

### Movimiento
```python
class Movimiento(models.Model):
   tipo_eleccion = (
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    )
    nombre = models.CharField(max_length=50, null=False, default='')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=tipo_eleccion, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField(default=timezone.now())
```
El modelo de Movimiento cuenta con los atributos de:
- Nombre: El nombre que tendrá cada movimiento
- Usuario: El usuario al que se asigna el movimiento, es una foreign key del modelo User de Django
- Tipo: El tipo de movimiento, que puede ser ingreso o gasto para asignarse
- Categoría: La categoría que se le asigna a cada movimiento pudiendo ser de cualquiera que el administrador agregue como categoría
- Monto: El monto que se asigna al movimiento
- Descripción: Descripción del movimiento (por ahora no se utiliza)
- Fecha: La fecha que se le asigna al movimiento para mantener un orden y saber cuando se realizó
---

## Vistas

### Vista Principal
```python
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
```
- Se requiere estar loggeado para acceder a esta vista, aquí se encuentran todos los movimientos del usuario
- Función para filtrar por tipo o por categoría
- Se pueden visualizar los ingresos y gastos totales, ademas de la diferencia entre ellos para tener un mejor control sobre los movimientos

### Vista Inicio de Sesión
```python
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
```

- Indica al usuario que debe ingresar nombre de usuario y contraseña para validar sus credenciales y darle acceso a la vista principal
- En caso de equivocarse aparecerá un error que indica que sus credenciales son incorrectas y debe volver a intentar el formulario
- Al tener un inicio de sesión correcto será redirigido a la vista principal donde podrá ver sus movimientos o agregar nuevos

### Vista de Registro
```python
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
```
- Se le pide al usuario un nombre y su contraseña, que deberá escribir dos veces para confirmar
- Al registrarse correctamente se le redigirá a la ventana principal con su nueva sesión
- En caso de equivocarse en el formulario se le indicará al usuario el problema para que vuelva nuevamente a ingresar sus datos

### Vista Cerrar Sesión
```python
@login_required
def signout(request):
    logout(request)
    return redirect('login')
```
- Al dar click en el botón de cerrar sesión activará esta vista que se encarga de la función que cierra por completo la sesión del usuario
- Se regresa al usuario a la vista de inicio de sesión para que vuelva a iniciar sesión o registrarse si asi lo desea

### Vista Crear Movimiento
```python
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
```
- Formulario para agregar un movimiento y registrarlo para el usuario que está realizando la acción
- El formulario cuenta con campos como nombre, tipo, categoría y fecha en que se realizó el gasto
- Al enviar el formulario correctamente se redirige a la vista principal donde será mostrado el nuevo movimiento agregado
- En caso de haber algún error se le indicará al usuario que ingrese datos validos

### Vista Borrar Movimiento
```python
@login_required
def borrar_movimiento(request, id):
    movimiento = get_object_or_404(Movimiento, pk=id, usuario=request.user)
    movimiento.delete()
    return redirect('home')
```
- Al ejecutar esta vista se busca el movimiento por su primary key y que pertenezca al usuario que la está llamando
- Cuando encuentra el movimiento lo elimina definitivamente y se redirige al usuario a la vista principal

### Vista Editar Movimiento
```python
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
```
- Se usa el mismo formulario que para crear movimientos, pero se rellena con los datos del movimiento seleccionado para editar
- Se puede modificar cualquier valor del formulario para después dar click en guardar y se registrarán correctamente los cambios
- Al guardar se redirige al usuario a la vista principal
---







