from django.contrib import admin
from .models import LogAccion, LogInventario

@admin.register(LogAccion)
class LogAccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_accion', 'modelo_afectado', 'id_objeto', 'fecha_accion', 'ip_address')
    list_filter = ('tipo_accion', 'modelo_afectado', 'fecha_accion')
    search_fields = ('usuario__username', 'descripcion', 'modelo_afectado')
    readonly_fields = ('usuario', 'tipo_accion', 'modelo_afectado', 'id_objeto', 'descripcion', 'fecha_accion', 'ip_address')
    ordering = ('-fecha_accion',)
    date_hierarchy = 'fecha_accion'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(LogInventario)
class LogInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'usuario', 'tipo_cambio', 'cantidad_anterior', 'cantidad_nueva', 'cantidad_cambiada', 'fecha_cambio')
    list_filter = ('tipo_cambio', 'fecha_cambio', 'producto__taller')
    search_fields = ('producto__modelo', 'usuario__username', 'motivo')
    readonly_fields = ('producto', 'usuario', 'tipo_cambio', 'cantidad_anterior', 'cantidad_nueva', 'cantidad_cambiada', 'motivo', 'fecha_cambio')
    ordering = ('-fecha_cambio',)
    date_hierarchy = 'fecha_cambio'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
