from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Producto, Etiqueta
from .serializers import (
    ProductoSerializer, EtiquetaSerializer,
    AjusteInventarioSerializer, RebajaInventarioSerializer,
    TrasladoInventarioSerializer
)
from talleres.models import Taller
from logs.models import LogInventario
from usuarios.utils import requiere_permiso
from django.db import models

# Create your views here.

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('taller').prefetch_related('etiquetas')
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Producto.objects.select_related('taller').prefetch_related('etiquetas')
        taller_id = self.request.query_params.get('taller', None)
        if taller_id:
            queryset = queryset.filter(taller_id=taller_id)
        return queryset
    
    @action(detail=True, methods=['post'], url_path='adicionar-stock')
    @requiere_permiso('editar')
    def adicionar_stock(self, request, pk=None):
        """Adiciona stock a un producto"""
        producto = self.get_object()
        serializer = AjusteInventarioSerializer(data=request.data)
        
        if serializer.is_valid():
            cantidad = serializer.validated_data['cantidad']
            motivo = serializer.validated_data.get('motivo', 'Adición de stock')
            
            with transaction.atomic():
                cantidad_anterior = producto.cantidad
                producto.cantidad += cantidad
                producto.save()
                
                # Crear log de inventario
                LogInventario.objects.create(
                    producto=producto,
                    usuario=request.user,
                    tipo_cambio='INGRESO',
                    cantidad_anterior=cantidad_anterior,
                    cantidad_nueva=producto.cantidad,
                    cantidad_cambiada=cantidad,
                    motivo=motivo
                )
            
            return Response({
                'message': f'Stock adicionado exitosamente. Nueva cantidad: {producto.cantidad}',
                'cantidad_anterior': cantidad_anterior,
                'cantidad_nueva': producto.cantidad,
                'cantidad_adicionada': cantidad
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='rebajar-stock')
    @requiere_permiso('editar')
    def rebajar_stock(self, request, pk=None):
        """Rebaja stock de un producto"""
        producto = self.get_object()
        serializer = RebajaInventarioSerializer(
            data=request.data,
            context={'producto': producto}
        )
        
        if serializer.is_valid():
            cantidad = serializer.validated_data['cantidad']
            motivo = serializer.validated_data.get('motivo', 'Rebaja de stock')
            
            with transaction.atomic():
                cantidad_anterior = producto.cantidad
                producto.cantidad -= cantidad
                producto.save()
                
                # Crear log de inventario
                LogInventario.objects.create(
                    producto=producto,
                    usuario=request.user,
                    tipo_cambio='SALIDA',
                    cantidad_anterior=cantidad_anterior,
                    cantidad_nueva=producto.cantidad,
                    cantidad_cambiada=-cantidad,
                    motivo=motivo
                )
            
            return Response({
                'message': f'Stock rebajado exitosamente. Nueva cantidad: {producto.cantidad}',
                'cantidad_anterior': cantidad_anterior,
                'cantidad_nueva': producto.cantidad,
                'cantidad_rebajada': cantidad
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='trasladar-stock')
    @requiere_permiso('editar')
    def trasladar_stock(self, request, pk=None):
        """Traslada stock de un producto a otro taller"""
        producto = self.get_object()
        serializer = TrasladoInventarioSerializer(
            data=request.data,
            context={'producto': producto}
        )
        
        if serializer.is_valid():
            cantidad = serializer.validated_data['cantidad']
            taller_destino_id = serializer.validated_data['taller_destino_id']
            motivo = serializer.validated_data.get('motivo', 'Traslado entre talleres')
            
            try:
                taller_destino = Taller.objects.get(id=taller_destino_id)
            except Taller.DoesNotExist:
                return Response(
                    {'error': 'Taller de destino no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            with transaction.atomic():
                # Rebajar del taller origen
                cantidad_anterior_origen = producto.cantidad
                producto.cantidad -= cantidad
                producto.save()
                
                # Crear o actualizar producto en taller destino
                producto_destino, created = Producto.objects.get_or_create(
                    taller=taller_destino,
                    modelo=producto.modelo,
                    defaults={
                        'descripcion': producto.descripcion,
                        'cantidad': cantidad,
                        'cantidad_minima': producto.cantidad_minima,
                        'precio_costo': producto.precio_costo,
                        'precio_venta': producto.precio_venta,
                        'etiquetas': producto.etiquetas.all()
                    }
                )
                
                if not created:
                    cantidad_anterior_destino = producto_destino.cantidad
                    producto_destino.cantidad += cantidad
                    producto_destino.save()
                else:
                    cantidad_anterior_destino = 0
                
                # Log para taller origen
                LogInventario.objects.create(
                    producto=producto,
                    usuario=request.user,
                    tipo_cambio='TRASLADO',
                    taller_origen=producto.taller,
                    taller_destino=taller_destino,
                    cantidad_anterior=cantidad_anterior_origen,
                    cantidad_nueva=producto.cantidad,
                    cantidad_cambiada=-cantidad,
                    motivo=motivo
                )
                
                # Log para taller destino
                LogInventario.objects.create(
                    producto=producto_destino,
                    usuario=request.user,
                    tipo_cambio='TRASLADO',
                    taller_origen=producto.taller,
                    taller_destino=taller_destino,
                    cantidad_anterior=cantidad_anterior_destino,
                    cantidad_nueva=producto_destino.cantidad,
                    cantidad_cambiada=cantidad,
                    motivo=motivo
                )
            
            return Response({
                'message': f'Stock trasladado exitosamente',
                'taller_origen': producto.taller.nombre,
                'taller_destino': taller_destino.nombre,
                'cantidad_trasladada': cantidad,
                'stock_restante_origen': producto.cantidad,
                'stock_total_destino': producto_destino.cantidad
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='stock-bajo')
    def stock_bajo(self, request):
        """Lista productos con stock bajo"""
        productos = self.get_queryset().filter(
            cantidad__lte=models.F('cantidad_minima')
        )
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    permission_classes = [IsAuthenticated]
    
    @requiere_permiso('crear')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @requiere_permiso('editar')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @requiere_permiso('editar')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @requiere_permiso('eliminar')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
