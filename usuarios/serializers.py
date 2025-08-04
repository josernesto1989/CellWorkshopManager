from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import PerfilUsuario, Rol
from talleres.models import Taller

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class TallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = ['id', 'nombre', 'direccion']

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    taller = TallerSerializer(read_only=True)
    rol_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    taller_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = PerfilUsuario
        fields = [
            'id', 'rol', 'rol_id', 'taller', 'taller_id', 'telefono', 
            'direccion', 'fecha_nacimiento', 'fecha_contratacion', 
            'activo', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_rol_id(self, value):
        if value is not None:
            try:
                Rol.objects.get(id=value)
            except Rol.DoesNotExist:
                raise serializers.ValidationError("Rol no encontrado")
        return value
    
    def validate_taller_id(self, value):
        if value is not None:
            try:
                Taller.objects.get(id=value)
            except Taller.DoesNotExist:
                raise serializers.ValidationError("Taller no encontrado")
        return value
    
    def update(self, instance, validated_data):
        rol_id = validated_data.pop('rol_id', None)
        taller_id = validated_data.pop('taller_id', None)
        
        if rol_id is not None:
            instance.rol_id = rol_id
        if taller_id is not None:
            instance.taller_id = taller_id
        
        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilUsuarioSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'perfil']
        read_only_fields = ['id']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Usuario inactivo")
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("Credenciales inválidas")
        else:
            raise serializers.ValidationError("Debe proporcionar username y password")

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    perfil = PerfilUsuarioSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 
            'first_name', 'last_name', 'perfil'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este username ya está en uso")
        return value
    
    def create(self, validated_data):
        password_confirm = validated_data.pop('password_confirm')
        perfil_data = validated_data.pop('perfil', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Crear perfil si se proporciona
        if perfil_data:
            PerfilUsuario.objects.create(usuario=user, **perfil_data)
        
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("Las nuevas contraseñas no coinciden")
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Contraseña actual incorrecta")
        return value 