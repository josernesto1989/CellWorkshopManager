from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Producto, Etiqueta
from logs.models import LogAccion, LogInventario
from inventario.middleware import get_current_user

# --- PRE SAVE: Guarda cantidad anterior ---
@receiver(pre_save, sender=Producto)
def set_old_cantidad(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Producto.objects.get(pk=instance.pk)
            instance._old_cantidad = old.cantidad
        except Producto.DoesNotExist:
            instance._old_cantidad = None
    else:
        instance._old_cantidad = None

@receiver(post_save, sender=Producto)
def log_producto_save(sender, instance, created, **kwargs):
    user = get_current_user()
    if user is None or not user.is_authenticated:
        return
    if created:
        LogAccion.objects.create(
            usuario=user,
            tipo_accion='CREAR',
            modelo_afectado='Producto',
            id_objeto=instance.id,
            descripcion=f'Producto creado: {instance.modelo}',
            ip_address=None
        )
        LogInventario.objects.create(
            producto=instance,
            usuario=user,
            tipo_cambio='INGRESO',
            cantidad_anterior=0,
            cantidad_nueva=instance.cantidad,
            cantidad_cambiada=instance.cantidad,
            motivo='Creación de producto',
        )
    else:
        LogAccion.objects.create(
            usuario=user,
            tipo_accion='ACTUALIZAR',
            modelo_afectado='Producto',
            id_objeto=instance.id,
            descripcion=f'Producto actualizado: {instance.modelo}',
            ip_address=None
        )
        # LogInventario solo si cambia la cantidad
        old_cantidad = getattr(instance, '_old_cantidad', None)
        if old_cantidad is not None and old_cantidad != instance.cantidad:
            LogInventario.objects.create(
                producto=instance,
                usuario=user,
                tipo_cambio='AJUSTE',
                cantidad_anterior=old_cantidad,
                cantidad_nueva=instance.cantidad,
                cantidad_cambiada=instance.cantidad - old_cantidad,
                motivo='Ajuste de inventario desde admin',
            )

@receiver(post_delete, sender=Producto)
def log_producto_delete(sender, instance, **kwargs):
    user = get_current_user()
    if user is None or not user.is_authenticated:
        return
    LogAccion.objects.create(
        usuario=user,
        tipo_accion='ELIMINAR',
        modelo_afectado='Producto',
        id_objeto=instance.id,
        descripcion=f'Producto eliminado: {instance.modelo}',
        ip_address=None
    )
    LogInventario.objects.create(
        producto=instance,
        usuario=user,
        tipo_cambio='SALIDA',
        cantidad_anterior=instance.cantidad,
        cantidad_nueva=0,
        cantidad_cambiada=-instance.cantidad,
        motivo='Eliminación de producto',
    )

# --- LOGS PARA ETIQUETA ---
@receiver(post_save, sender=Etiqueta)
def log_etiqueta_save(sender, instance, created, **kwargs):
    user = get_current_user()
    if user is None or not user.is_authenticated:
        return
    if created:
        LogAccion.objects.create(
            usuario=user,
            tipo_accion='CREAR',
            modelo_afectado='Etiqueta',
            id_objeto=instance.id,
            descripcion=f'Etiqueta creada: {instance.nombre}',
            ip_address=None
        )
    else:
        LogAccion.objects.create(
            usuario=user,
            tipo_accion='ACTUALIZAR',
            modelo_afectado='Etiqueta',
            id_objeto=instance.id,
            descripcion=f'Etiqueta actualizada: {instance.nombre}',
            ip_address=None
        )

@receiver(post_delete, sender=Etiqueta)
def log_etiqueta_delete(sender, instance, **kwargs):
    user = get_current_user()
    if user is None or not user.is_authenticated:
        return
    LogAccion.objects.create(
        usuario=user,
        tipo_accion='ELIMINAR',
        modelo_afectado='Etiqueta',
        id_objeto=instance.id,
        descripcion=f'Etiqueta eliminada: {instance.nombre}',
        ip_address=None
    ) 