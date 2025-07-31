from django.db import models
from django.contrib.auth.models import User
from talleres.models import Taller

# Create your models here.

# Rol define los diferentes tipos de usuarios en el sistema.
class Rol(models.Model):
    ROLES_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('GERENTE', 'Gerente'),
        ('TECNICO', 'Técnico'),
        ('VENDEDOR', 'Vendedor'),
        ('INVENTARIO', 'Encargado de Inventario'),
        ('AUDITOR', 'Auditor'),
    ]
    
    nombre = models.CharField(max_length=20, choices=ROLES_CHOICES, unique=True)
    descripcion = models.TextField(blank=True)
    permisos_crear = models.BooleanField(default=False)
    permisos_editar = models.BooleanField(default=False)
    permisos_eliminar = models.BooleanField(default=False)
    permisos_ver_logs = models.BooleanField(default=False)
    permisos_administrar_usuarios = models.BooleanField(default=False)
    
    def __str__(self):
         return self.nombre

# PerfilUsuario extiende el modelo User de Django con información adicional.
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    taller = models.ForeignKey(Taller, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_contratacion = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.rol.nombre if self.rol else 'Sin rol'}"
    
    def tiene_permiso(self, permiso):
        """Verifica si el usuario tiene un permiso específico."""
        if not self.rol:
            return False
        
        return getattr(self.rol, f'permisos_{permiso}', False)
    
    def puede_crear(self):
        return self.tiene_permiso('crear')
    
    def puede_editar(self):
        return self.tiene_permiso('editar')
    
    def puede_eliminar(self):
        return self.tiene_permiso('eliminar')
    
    def puede_ver_logs(self):
        return self.tiene_permiso('ver_logs')
    
    def puede_administrar_usuarios(self):
        return self.tiene_permiso('administrar_usuarios')
