from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

def requiere_permiso(permiso):
    """
    Decorador para verificar si un usuario tiene un permiso específico.
    Uso: @requiere_permiso('crear')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            try:
                if hasattr(request.user, 'perfil') and request.user.perfil.tiene_permiso(permiso):
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, f'No tienes permisos para realizar esta acción.')
                    return HttpResponseForbidden("Acceso denegado")
            except Exception:
                messages.error(request, 'Error al verificar permisos.')
                return HttpResponseForbidden("Error de permisos")
        return _wrapped_view
    return decorator

def requiere_rol(rol_nombre):
    """
    Decorador para verificar si un usuario tiene un rol específico.
    Uso: @requiere_rol('ADMIN')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            try:
                if (hasattr(request.user, 'perfil') and 
                    request.user.perfil.rol and 
                    request.user.perfil.rol.nombre == rol_nombre):
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, f'Se requiere el rol {rol_nombre} para esta acción.')
                    return HttpResponseForbidden("Acceso denegado")
            except Exception:
                messages.error(request, 'Error al verificar rol.')
                return HttpResponseForbidden("Error de permisos")
        return _wrapped_view
    return decorator

def es_admin(user):
    """Verifica si un usuario es administrador."""
    return (user.is_authenticated and 
            hasattr(user, 'perfil') and 
            user.perfil.rol and 
            user.perfil.rol.nombre == 'ADMIN')

def es_gerente(user):
    """Verifica si un usuario es gerente."""
    return (user.is_authenticated and 
            hasattr(user, 'perfil') and 
            user.perfil.rol and 
            user.perfil.rol.nombre == 'GERENTE')

def puede_ver_taller(user, taller):
    """Verifica si un usuario puede ver/editar un taller específico."""
    if es_admin(user) or es_gerente(user):
        return True
    
    return (user.is_authenticated and 
            hasattr(user, 'perfil') and 
            user.perfil.taller == taller) 