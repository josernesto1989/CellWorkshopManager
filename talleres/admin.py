from django.contrib import admin
from .models import Taller

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'email', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('nombre', 'direccion', 'telefono', 'email')
    readonly_fields = ('fecha_creacion',)
    ordering = ('nombre',)
