from django.db import models
from django.contrib.auth.models import User
from talleres.models import Taller
from inventario.models import Producto

# Create your models here.

# LogAccion registra todas las acciones realizadas por los usuarios en el sistema.
class LogAccion(models.Model):
    TIPO_ACCION_CHOICES = [
        ('CREAR', 'Crear'),
        ('ACTUALIZAR', 'Actualizar'),
        ('ELIMINAR', 'Eliminar'),
        ('CONSULTAR', 'Consultar'),
        ('LOGIN', 'Iniciar sesión'),
        ('LOGOUT', 'Cerrar sesión'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs_acciones')  # Usuario que realizó la acción
    tipo_accion = models.CharField(max_length=20, choices=TIPO_ACCION_CHOICES)  # Tipo de acción realizada
    modelo_afectado = models.CharField(max_length=50)  # Nombre del modelo afectado (ej: 'Taller', 'Producto')
    id_objeto = models.IntegerField()  # ID del objeto afectado
    descripcion = models.TextField()  # Descripción detallada de la acción
    fecha_accion = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la acción
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Dirección IP del usuario
    
    def __str__(self):
        return f"{self.usuario.username} - {self.tipo_accion} - {self.modelo_afectado} - {self.fecha_accion}"

# LogInventario registra específicamente los cambios en el inventario de productos.
class LogInventario(models.Model):
    TIPO_CAMBIO_CHOICES = [
        ('INGRESO', 'Ingreso de stock'),
        ('SALIDA', 'Salida de stock'),
        ('AJUSTE', 'Ajuste de inventario'),
        ('TRASLADO', 'Traslado entre talleres'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='logs_inventario')  # Producto afectado
    taller_origen = models.ForeignKey(Taller, on_delete=models.CASCADE, related_name='logs_origen', null=True, blank=True)  # Taller de origen (para traslados)
    taller_destino = models.ForeignKey(Taller, on_delete=models.CASCADE, related_name='logs_destino', null=True, blank=True)  # Taller de destino (para traslados)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs_inventario')  # Usuario que realizó el cambio
    tipo_cambio = models.CharField(max_length=20, choices=TIPO_CAMBIO_CHOICES)  # Tipo de cambio realizado
    cantidad_anterior = models.PositiveIntegerField()  # Cantidad antes del cambio
    cantidad_nueva = models.PositiveIntegerField()  # Cantidad después del cambio
    cantidad_cambiada = models.IntegerField()  # Diferencia (positiva para ingresos, negativa para salidas)
    motivo = models.TextField(blank=True)  # Motivo del cambio
    fecha_cambio = models.DateTimeField(auto_now_add=True)  # Fecha y hora del cambio
    
    def __str__(self):
        return f"{self.producto.modelo} - {self.tipo_cambio} - {self.cantidad_cambiada} - {self.fecha_cambio}"
