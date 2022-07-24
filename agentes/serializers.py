from rest_framework import serializers

from agentes.models import Agente, PlanMembresia, GestionDocumental
from zonas.serializers import ZonaLiteSerializer, MunicipioSerializer


class AgenteLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agente
        fields = ('id', 'nombre', 'apellido', 'email', 'foto_perfil', 'slug', 'telefono_contacto', 'zonificacion',
                  'redes_sociales', 'descripcion_perfil', 'numero_avaluo', 'municipio', 'fecha_inicio_plan',
                  'plan_membresia')


class AgentePATCHSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agente
        fields = ('id', 'numero_avaluo', 'municipio')


class PlanMembresiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanMembresia
        fields = ('id', 'nombre', 'nombre', 'precio_promocion', 'precio_fijo', 'fecha_creacion', 'fecha_modificacion')


class AgenteSerializer(serializers.ModelSerializer):
    ciudades = ZonaLiteSerializer(read_only=True, many=True)
    zonas_dommun = ZonaLiteSerializer(read_only=True, many=True)
    municipio_obj = MunicipioSerializer(source='municipio', read_only=True)
    plan_membresia_obj = PlanMembresiaSerializer(source='plan_membresia', read_only=True)

    class Meta:
        model = Agente
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GestionDocumentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestionDocumental
        fields = ('id', 'nombre', 'documento_subido', 'categoria', 'fecha_modificacion')
