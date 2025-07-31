from django.db import models
from talleres.models import Taller

# Create your models here.

# Etiqueta representa una categoría o tag que puede asociarse a varios productos.
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# Producto representa un ítem de inventario asociado a un taller específico.
class Producto(models.Model):
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE, related_name='productos')  # Taller al que pertenece el producto
    modelo = models.CharField(max_length=100)  # Modelo o nombre del producto
    descripcion = models.TextField(blank=True)  # Descripción opcional
    cantidad = models.PositiveIntegerField(default=0)  # Cantidad en stock
    cantidad_minima = models.PositiveIntegerField(default=0)  # Stock mínimo recomendado
    precio_costo = models.IntegerField(help_text="Valor en centavos")  # Costo de adquisición en centavos
    precio_venta = models.IntegerField(help_text="Valor en centavos")  # Precio de venta en centavos
    fecha_ingreso = models.DateTimeField(auto_now_add=True)  # Fecha de ingreso al inventario
    etiquetas = models.ManyToManyField('Etiqueta', blank=True, related_name='productos')  # Etiquetas asociadas

    def __str__(self):
        return f"{self.modelo} ({getattr(self.taller, 'nombre', '')})"
