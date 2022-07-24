from rest_framework import serializers

from clientes.serializers import AgenteUserSerializer
from propiedades.serializers import PropiedadGETSerializer, LoteLiteMapSerializer, ViviendaLiteMapSerializer, \
    ComercialLiteMapSerializer, IndustrialLiteMapSerializer
from publicaciones.models import PublicacionVivienda, PublicacionLotes, PublicacionComercial, PublicacionIndustrial, \
    Publicacion


# **********************************************'
# Publicación Vivienda Serializer'
# **********************************************'
class PublicacionViviendaSerializer(serializers.ModelSerializer):
    agente_obj = AgenteUserSerializer(source='agente', read_only=True)
    propiedad_obj = PropiedadGETSerializer(source='propiedad', read_only=True)

    class Meta:
        model = PublicacionVivienda


# **********************************************'
# Publicación Lotes Serializer'
# **********************************************'
class PublicacionLotesSerializer(serializers.ModelSerializer):
    agente_obj = AgenteUserSerializer(source='agente', read_only=True)
    propiedad_obj = PropiedadGETSerializer(source='propiedad', read_only=True)

    class Meta:
        model = PublicacionLotes


# **********************************************'
# Publicación Comercial Serializer'
# **********************************************'
class PublicacionComercialSerializer(serializers.ModelSerializer):
    agente_obj = AgenteUserSerializer(source='agente', read_only=True)
    propiedad_obj = PropiedadGETSerializer(source='propiedad', read_only=True)

    class Meta:
        model = PublicacionComercial


# **********************************************'
# Publicación Industrial Serializer'
# **********************************************'
class PublicacionIndustrialSerializer(serializers.ModelSerializer):
    agente_obj = AgenteUserSerializer(source='agente', read_only=True)
    propiedad_obj = PropiedadGETSerializer(source='propiedad', read_only=True)

    class Meta:
        model = PublicacionIndustrial


# **********************************************'
# Publicación Vivienda Minimal Serializer'
# **********************************************'
class PublicacionViviendaMinimalSerializer(serializers.ModelSerializer):
    propiedad_obj = ViviendaLiteMapSerializer(source='propiedad', read_only=True)

    class Meta:
        model = PublicacionVivienda
        fields = ('id', 'propiedad_obj', 'precio', 'precio_admon', 'tipo_negocio', 'bajo_precio', 'visitas', 'estado')


# **********************************************'
# Publicación Lotes Minimal Serializer'
# **********************************************'
class PublicacionLotesMinimalSerializer(serializers.ModelSerializer):
    propiedad_obj = LoteLiteMapSerializer(source='propiedad', read_only=True)

    class Meta:
        model = PublicacionLotes
        fields = ('id', 'propiedad_obj', 'precio', 'precio_admon', 'tipo_negocio', 'bajo_precio', 'visitas', 'estado')


# **********************************************'
# Publicación Comercial Minimal Serializer'
# **********************************************'
class PublicacionComercialMinimalSerializer(serializers.ModelSerializer):
    propiedad_obj = ComercialLiteMapSerializer(source='propiedad', read_only=True)

    class Meta:
        model = PublicacionComercial
        fields = ('id', 'propiedad_obj', 'precio', 'precio_admon', 'tipo_negocio', 'bajo_precio', 'visitas', 'estado')


# **********************************************'
# Publicación Industrial Minimal Serializer'
# **********************************************'
class PublicacionIndustrialMinimalSerializer(serializers.ModelSerializer):
    propiedad_obj = IndustrialLiteMapSerializer(source='propiedad', read_only=True)

    class Meta:
        model = PublicacionIndustrial
        fields = ('id', 'propiedad_obj', 'precio', 'precio_admon', 'tipo_negocio', 'bajo_precio', 'visitas', 'estado')


class PublicacionGETSerializer(serializers.ModelSerializer):
    agente_obj = AgenteUserSerializer(source='agente', read_only=True)
    propiedad_obj = PropiedadGETSerializer(source='propiedad', read_only=True)

    class Meta:
        model = Publicacion

    def to_representation(self, obj):
        """
        Because Propiedad is Polymorphic
        """
        if isinstance(obj, PublicacionVivienda):
            return PublicacionViviendaSerializer(obj, context=self.context).to_representation(obj)
        return super(PublicacionGETSerializer, self).to_representation(obj)


class PublicacionGETSerializerComercial(serializers.ModelSerializer):
    agente_obj = AgenteUserSerializer(source='agente', read_only=True)
    propiedad_obj = PropiedadGETSerializer(source='propiedad', read_only=True)

    class Meta:
        model = Publicacion

    def to_representation(self, obj):
        if isinstance(obj, PublicacionComercial):
            return PublicacionComercialSerializer(obj, context=self.context).to_representation(obj)
        return super(PublicacionGETSerializer, self).to_representation(obj)


class PublicacionGETSerializerIndustrial(serializers.ModelSerializer):
    agente_obj = AgenteUserSerializer(source='agente', read_only=True)
    propiedad_obj = PropiedadGETSerializer(source='propiedad', read_only=True)

    class Meta:
        model = Publicacion

    def to_representation(self, obj):
        if isinstance(obj, PublicacionIndustrial):
            return PublicacionIndustrialSerializer(obj, context=self.context).to_representation(obj)
        return super(PublicacionGETSerializer, self).to_representation(obj)


class PublicacionGETSerializerLotes(serializers.ModelSerializer):
    agente_obj = AgenteUserSerializer(source='agente', read_only=True)
    propiedad_obj = PropiedadGETSerializer(source='propiedad', read_only=True)

    class Meta:
        model = Publicacion

    def to_representation(self, obj):
        if isinstance(obj, PublicacionLotes):
            return PublicacionLotesSerializer(obj, context=self.context).to_representation(obj)
        return super(PublicacionGETSerializer, self).to_representation(obj)
