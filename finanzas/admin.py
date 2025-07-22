from django.contrib import admin
from .models import Movimiento, Categoria

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Movimiento)