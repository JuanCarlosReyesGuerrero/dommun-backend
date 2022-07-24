from django.contrib.auth.models import User, Group
from rest_framework import serializers

from agentes.models import Agente
from clientes.models import Cliente, Necesidad, PropiedadNecesidad
from zonas.serializers import ZonaLiteSerializer


class AgenteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agente


class ClienteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class UserSerializer(serializers.ModelSerializer):
    groups = GroupsSerializer(many=True)
    cliente = ClienteUserSerializer(many=True)
    agente = AgenteUserSerializer(many=True)

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}


class PropiedadNecesidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropiedadNecesidad


#class PropiedadNecesidadConPropSerializer(serializers.ModelSerializer):
#    propiedad = InmuebleLiteMapSerializer(read_only=True)

#    class Meta:
#        model = PropiedadNecesidad


class PropiedadNecesidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropiedadNecesidad


class NecesidadSerializer(serializers.ModelSerializer):
    #propiedades = PropiedadNecesidadConPropSerializer(many=True, read_only=True)
    zonas_objs = ZonaLiteSerializer(source='zonas', many=True, read_only=True)

    class Meta:
        model = Necesidad


class ClienteSerializer(serializers.ModelSerializer):
    necesidad = NecesidadSerializer(source='get_current_necesidad', read_only=True)
    agente_obj = AgenteUserSerializer(source='agente', read_only=True)

    class Meta:
        model = Cliente
