from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
import json

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware personalizado para manejar autenticación JWT
    y proporcionar respuestas de error consistentes
    """
    
    def process_request(self, request):
        # Solo procesar requests a la API
        if not request.path.startswith('/api/'):
            return None
        
        # Excluir endpoints de autenticación
        auth_endpoints = [
            '/api/usuarios/auth/login/',
            '/api/usuarios/auth/refresh/',
            '/api/usuarios/auth/register/',
        ]
        
        if request.path in auth_endpoints:
            return None
        
        # Verificar token JWT en el header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                'error': 'Token de autenticación requerido',
                'detail': 'Debe incluir un token Bearer en el header Authorization'
            }, status=401)
        
        token = auth_header.split(' ')[1]
        
        try:
            # Validar token
            AccessToken(token)
        except (InvalidToken, TokenError) as e:
            return JsonResponse({
                'error': 'Token inválido',
                'detail': str(e)
            }, status=401)
        
        return None
    
    def process_response(self, request, response):
        # Agregar headers CORS para desarrollo
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response 