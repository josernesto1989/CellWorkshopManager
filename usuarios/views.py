from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import PerfilUsuario, Rol
from .serializers import (
    UserSerializer, PerfilUsuarioSerializer, 
    LoginSerializer, RegisterSerializer
)

# Create your views here.

class LoginView(TokenObtainPairView):
    """Vista personalizada para login con JWT"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        # Obtener información del perfil
        try:
            perfil = user.perfil
        except PerfilUsuario.DoesNotExist:
            perfil = None
        
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'perfil': PerfilUsuarioSerializer(perfil).data if perfil else None
            }
        }, status=status.HTTP_200_OK)

class RefreshTokenView(TokenRefreshView):
    """Vista para refrescar tokens JWT"""
    permission_classes = [AllowAny]

class LogoutView(generics.GenericAPIView):
    """Vista para logout (invalidar tokens)"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Logout exitoso'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Token inválido'
            }, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    """Vista para registro de usuarios"""
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'perfil': PerfilUsuarioSerializer(user.perfil).data if hasattr(user, 'perfil') else None
            }
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Obtener perfil del usuario autenticado"""
    try:
        perfil = request.user.perfil
        serializer = PerfilUsuarioSerializer(perfil)
        return Response(serializer.data)
    except PerfilUsuario.DoesNotExist:
        return Response({
            'error': 'Perfil no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Actualizar perfil del usuario autenticado"""
    try:
        perfil = request.user.perfil
        serializer = PerfilUsuarioSerializer(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except PerfilUsuario.DoesNotExist:
        return Response({
            'error': 'Perfil no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    """Obtener permisos del usuario autenticado"""
    try:
        perfil = request.user.perfil
        return Response({
            'puede_crear': perfil.puede_crear(),
            'puede_editar': perfil.puede_editar(),
            'puede_eliminar': perfil.puede_eliminar(),
            'puede_ver_logs': perfil.puede_ver_logs(),
            'puede_administrar_usuarios': perfil.puede_administrar_usuarios(),
            'rol': perfil.rol.nombre if perfil.rol else None,
            'taller': perfil.taller.nombre if perfil.taller else None
        })
    except PerfilUsuario.DoesNotExist:
        return Response({
            'error': 'Perfil no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Cambiar contraseña del usuario autenticado"""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({
            'message': 'Contraseña cambiada exitosamente'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
