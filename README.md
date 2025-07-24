# Control de Gastos – Django

Una aplicación web sencilla para registrar, categorizar y visualizar tus gastos personales, construida con Django.

## 🌍 Demo en Línea

Puedes ver la app desplegada en [control-de-gastos.azurewebsites.net](https://control-de-gastos.azurewebsites.net/)

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

## Templates

### Base
```HTML
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Control de Gastos</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" />
  </head>
  <body>
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
      <div class="container">
        <a class="navbar-brand" href="/">Control de Gastos App</a>
        
        <div class="text-center text-xs-start" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            {% if user.is_authenticated %}
              <li class="navlink-item">
                <a class="nav-link" href="{% url 'home' %}">Inicio</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{% url 'agregar' %}">Agregar Movimiento</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{% url 'logout' %}">Cerrar Sesión</a>
              </li>
            {% else %}
              <li class="nav-item">
                <a class="nav-link" href="{% url 'login' %}">Inicio de Sesión</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{% url 'signup' %}">Registrarse</a>
              </li>
            {% endif %}
          </ul>
        </div>
      </div>
    </nav>

    <nav>
      <ul></ul>
    </nav>
    {% block content %}

    {% endblock %}
  </body>
</html>
```
- Navbar para moverse entre vistas de la aplicación

### Home
```HTML
{% extends "base.html" %}
{% block content %}
<main class="container mb-4">
    <h1>Movimientos de <span class="fw-bold text-secondary text-decoration-underline">{{usuario|capfirst}}</span></h1>
    <h3>Ingresos: <span class="text-success">${{ingresos}}</span></h3>
    <h3>Gastos: <span class="text-danger">${{gastos}}</span></h3>
    <h3>Diferencia: <span class="fw-bold">${{diferencia}}</span></h3>

    <form action="" method="POST">
        {% csrf_token %}
        <div>
            <label for="filtro">Filtrar por Tipo:</label>
            <select name="filtro" id="filtro" onchange="this.form.submit()" class="form-control mb-3">
                <option value="todos" {% if filtro_tipo == 'todos' %}selected{% endif %}>Todos</option>
                <option value="gasto" {% if filtro_tipo == 'gasto' %}selected{% endif %}>Gasto</option>
                <option value="ingreso" {% if filtro_tipo == 'ingreso' %}selected{% endif %}>Ingreso</option>
            </select>
        </div>
        <div class="mb-3">
            <label for="filtro_categoria">Filtrar por categoría:</label>
            <select name="filtro_categoria" id="filtro_categoria" class="form-select" onchange="this.form.submit()">
                <option value="todas" {% if filtro_categoria == 'todas' %}selected{% endif %}>Todas</option>
                {% for cat in categorias %}
                <option value="{{ cat.id }}" {% if filtro_categoria == cat.id|stringformat:"s" %}selected{% endif %}>
                    {{ cat.nombre }}
                </option>
                {% endfor %}
            </select>
        </div>
    </form>
    <div class="row">
        {% for movimiento in movimientos %}
        <div class="col-md-4 col-sm-6 mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title fw-bold">-- {{ movimiento.nombre }} --</h5>
                    <p><strong>Fecha:</strong> {{ movimiento.fecha }}</p>
                    <p><strong>Tipo:</strong> <span class="fw-bold {% if movimiento.tipo == 'ingreso' %} text-success {% else %} text-danger {% endif %}">{{ movimiento.tipo|upper }}</span></p>
                    {% if movimiento.categoria %}
                    <p><strong>Categoría:</strong> {{ movimiento.categoria }}</p>
                    {% endif %}
                    <p><strong>Monto:</strong> ${{ movimiento.monto }}</p>
                    <a href="{% url 'borrar_movimiento' movimiento.id %}" class="btn btn-danger mt-2">Eliminar</a>
                    <a href="{% url 'editar_movimiento' movimiento.id %}" class="btn btn-secondary mt-2">Editar</a>
                </div>
            </div>
        </div>
        {% empty %}
        <h4>No hay movimientos aún, pruebe agregando alguno.</h4>
        {% endfor %}
    </div>
</main>
{% endblock content %}
```
- Se muestran los diferentes movimientos con sus características
- Se muestran los filtros para elegir que movimientos prefieres observar
- Se muestran los ingresos totales, los gastos totales y la diferencia
- Desde aquí se eliminan o editan los movimientos

### Inicio de Sesión
```HTML
{% extends "base.html" %}
{% block content %}
<main class="container">
    <div class="row">
        <div class="col-md-4 offset-md-4">
            <h1 class="text-center">Iniciar Sesión</h1>
            <form action="" method="POST">
                {{error}}
                <br>
                {% csrf_token %}
                <label for="username">Usuario:</label>
                <div>
                    <input class="w-100 form-control" type="text" name="username" id="username">
                </div>
                <label for="password">Contraseña:</label>
                <div class="mb-2">
                    <input class="w-100 form-control" type="password" name="password" id="password">
                </div>
                <button class="btn btn-dark">Iniciar sesión</button>
            </form>
            <br>
            <a class="text-decoration-none btn btn-secondary" href="/signup/">Click aquí para registrarse</a>
        </div>
    </div>
</main>
{% endblock content %}
```
- Formulario de inicio de sesión
- Se ingresa usuario y contraseña para ingresar

### Registrarse
```HTML
{% extends "base.html" %}
{% block content %}
<main class="container">
    <div class="row">
        <div class="col-md-4 offset-md-4">
            <h1 class="text-center">Registrarse</h1>
            <form action="" method="POST">
                {{error}}
                <br>
                {% csrf_token %}
                <label for="username">Usuario:</label>
                <div>
                    <input class="w-100 form-control" type="text" name="username" id="username">
                </div>
                <label for="password1">Contraseña:</label>
                <div>
                    <input class="w-100 form-control" type="password" name="password1" id="password1">
                </div>
                <label for="password2">Confirma tu Contraseña:</label>
                <div class="mb-2">
                    <input class="w-100 form-control" type="password" name="password2" id="password2">
                </div>
                <button class="btn btn-dark">Registrarse</button>
            </form>
        </div>
    </div>
</main>
{% endblock content %}
```
- Formulario para registrarse en la aplicación
- Se ingresan nombre de usuario y contraseña dos veces para confirmar

### Crear Movimiento
```HTML
{% extends "base.html" %}
{% block content %}
<main class="container">
    <div class="row">
        <div class="col-md-4 offset-md-4 mb-4">
            <h1>Crear Movimiento</h1>
            <form action="" method="POST">
                {{error}}
                {% csrf_token %}
                {{form.as_p}}
                <button class="btn btn-dark">Agregar</button>
            </form>
        </div>
    </div>
</main>
{% endblock content %}
```
- Formulario para crear un movimiento nuevo
- Se debe ingresar nombre, categoria, tipo y fecha en que se realizó el movimiento

### Editar Movimiento
```HTML
{% extends "base.html" %}
{% block content %}
<main class="container">
    <div class="row">
        <div class="col-md-4 offset-md-4 mb-4">
            <h1>Editar Movimiento</h1>
            <form action="" method="POST">
                {{error}}
                {% csrf_token %}
                {{form.as_p}}
                <button class="btn btn-dark">Guardar</button>
            </form>
        </div>
    </div>
</main>
{% endblock content %}
```
- Formulario para editar movimientos
- Se rellena automáticamente con los datos del movimiento seleccionado
- Se puede editar cualquier dato y se le da en el botón guardar para conservar los cambios

---


