from django.contrib import admin
from .models import Etiqueta, Producto

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'taller', 'cantidad', 'cantidad_minima', 'precio_costo', 'precio_venta', 'fecha_ingreso')
    list_filter = ('taller', 'etiquetas', 'fecha_ingreso')
    search_fields = ('modelo', 'descripcion', 'taller__nombre')
    readonly_fields = ('fecha_ingreso',)
    filter_horizontal = ('etiquetas',)
    ordering = ('modelo',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('taller')
