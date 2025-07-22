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
├── config/               # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── gastos/               # Aplicación principal
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── static/               # Archivos estáticos
├── templates/            # Plantillas base
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---
