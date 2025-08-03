from rest_framework import serializers
from .models import Producto, Etiqueta
from talleres.models import Taller

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class TallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    taller = TallerSerializer(read_only=True)
    taller_id = serializers.IntegerField(write_only=True)
    etiquetas = EtiquetaSerializer(many=True, read_only=True)
    etiquetas_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Producto
        fields = [
            'id', 'taller', 'taller_id', 'modelo', 'descripcion',
            'cantidad', 'cantidad_minima', 'precio_costo', 'precio_venta',
            'fecha_ingreso', 'etiquetas', 'etiquetas_ids'
        ]
        read_only_fields = ['id', 'fecha_ingreso']

    def create(self, validated_data):
        etiquetas_ids = validated_data.pop('etiquetas_ids', [])
        producto = Producto.objects.create(**validated_data)
        if etiquetas_ids:
            producto.etiquetas.set(etiquetas_ids)
        return producto

    def update(self, instance, validated_data):
        etiquetas_ids = validated_data.pop('etiquetas_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if etiquetas_ids is not None:
            instance.etiquetas.set(etiquetas_ids)
        
        return instance

class AjusteInventarioSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(min_value=1)
    motivo = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value

class RebajaInventarioSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(min_value=1)
    motivo = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value
    
    def validate(self, data):
        producto = self.context.get('producto')
        if producto and data['cantidad'] > producto.cantidad:
            raise serializers.ValidationError(
                f"No hay suficiente stock. Disponible: {producto.cantidad}, Solicitado: {data['cantidad']}"
            )
        return data

class TrasladoInventarioSerializer(serializers.Serializer):
    taller_destino_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)
    motivo = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value
    
    def validate(self, data):
        producto = self.context.get('producto')
        if producto and data['cantidad'] > producto.cantidad:
            raise serializers.ValidationError(
                f"No hay suficiente stock para trasladar. Disponible: {producto.cantidad}, Solicitado: {data['cantidad']}"
            )
        return data 