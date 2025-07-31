from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Rol, PerfilUsuario

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'permisos_crear', 'permisos_editar', 'permisos_eliminar', 'permisos_ver_logs', 'permisos_administrar_usuarios')
    list_filter = ('permisos_crear', 'permisos_editar', 'permisos_eliminar', 'permisos_ver_logs', 'permisos_administrar_usuarios')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    fk_name = 'usuario'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol', 'get_taller')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'perfil__rol', 'perfil__taller')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_rol(self, obj):
        return obj.perfil.rol.nombre if hasattr(obj, 'perfil') and obj.perfil.rol else 'Sin rol'
    get_rol.short_description = 'Rol'
    
    def get_taller(self, obj):
        return obj.perfil.taller.nombre if hasattr(obj, 'perfil') and obj.perfil.taller else 'Sin taller'
    get_taller.short_description = 'Taller'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
