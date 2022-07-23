from rest_framework import serializers

from zonas.models import Zona, Departamento, Municipio


class ZonaLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = ('id', 'nombre')


class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = ('id', 'slug', 'nombre', 'tipo_zona', 'zonas_dommun')


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ('id', 'nombre')


class MunicipioSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer(read_only=True)

    class Meta:
        model = Municipio
        fields = (
            'id', 'codigo', 'nombre', 'departamento')
