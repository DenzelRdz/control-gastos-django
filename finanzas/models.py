from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

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
    fecha = models.DateField()
    
    def __str__(self):
        return f'{self.nombre} - {self.tipo} - {self.usuario}'
