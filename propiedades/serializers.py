from rest_framework import serializers

from clientes.serializers import ClienteSerializer, AgenteUserSerializer
from propiedades.models import Caracteristica, DocumentoPropiedad, Fotografia, Vivienda, Comercial, Industrial, Lotes, \
    Propiedad
from publicaciones.models import PublicacionVivienda, PublicacionComercial, PublicacionIndustrial, PublicacionLotes
from zonas.serializers import MunicipioSerializer


class CaracteristicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristica


class DocumentoPropiedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoPropiedad


#class FotografiaSerializer(serializers.ModelSerializer):
#    image = VersatileImageFieldSerializer(
#        sizes='fotografias'
#    )

#    class Meta:
#        model = Fotografia


class ViviendaSerializer(serializers.ModelSerializer):
    #fotografias = FotografiaSerializer(many=True, read_only=True)
    propietario_obj = ClienteSerializer(source='propietario', read_only=True)
    municipio_obj = MunicipioSerializer(source='municipio', read_only=True)

    class Meta:
        model = Vivienda


class ComercialSerializer(serializers.ModelSerializer):
   # fotografias = FotografiaSerializer(many=True, read_only=True)
    propietario_obj = ClienteSerializer(source='propietario', read_only=True)
    municipio_obj = MunicipioSerializer(source='municipio', read_only=True)

    class Meta:
        model = Comercial


class IndustrialSerializer(serializers.ModelSerializer):
  #  fotografias = FotografiaSerializer(many=True, read_only=True)
    propietario_obj = ClienteSerializer(source='propietario', read_only=True)
    municipio_obj = MunicipioSerializer(source='municipio', read_only=True)

    class Meta:
        model = Industrial


class LotesSerializer(serializers.ModelSerializer):
   # fotografias = FotografiaSerializer(many=True, read_only=True)
    propietario_obj = ClienteSerializer(source='propietario', read_only=True)
    municipio_obj = MunicipioSerializer(source='municipio', read_only=True)

    class Meta:
        model = Lotes


class ViviendaLiteMapSerializer(serializers.ModelSerializer):
   # fotografia_obj = FotografiaSerializer(source='get_fotografiaPrincipal', read_only=True)

    class Meta:
        model = Vivienda
        fields = (
            'id', 'habitaciones', 'banos', 'area_construida', 'agente', 'fotografia_obj', 'direccion',
            'tipo_vivienda', 'estacionamientos_totales', 'banos_sociales', 'estacionamientos_cubiertos',
            'estacionamientos_descubiertos', 'municipio')


class LoteLiteMapSerializer(serializers.ModelSerializer):
   # fotografia_obj = FotografiaSerializer(source='get_fotografiaPrincipal', read_only=True)

    class Meta:
        model = Lotes
        fields = (
            'id', 'tipo', 'area_lote', 'agente',  'fotografia_obj', 'direccion', 'municipio')


class ComercialLiteMapSerializer(serializers.ModelSerializer):
   # fotografia_obj = FotografiaSerializer(source='get_fotografiaPrincipal', read_only=True)

    class Meta:
        model = Comercial
        fields = (
            'id', 'espacios', 'banos', 'area_construida', 'agente',  'fotografia_obj', 'direccion',
            'tipo', 'estacionamientos_totales', 'estacionamientos_cubiertos',
            'estacionamientos_descubiertos', 'municipio')


class IndustrialLiteMapSerializer(serializers.ModelSerializer):
  #  fotografia_obj = FotografiaSerializer(source='get_fotografiaPrincipal', read_only=True)

    class Meta:
        model = Industrial
        fields = (
            'id', 'espacios', 'banos', 'area_construida', 'agente',  'fotografia_obj', 'direccion',
            'tipo', 'municipio')


class PublicacionViviendaMinimalSinPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicacionVivienda
        fields = ('id', 'precio', 'precio_admon', 'tipo_negocio', 'bajo_precio', 'visitas')


class PublicacionComercialMinimalSinPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicacionComercial
        fields = ('id', 'precio', 'precio_admon', 'tipo_negocio', 'bajo_precio', 'visitas')


class PublicacionIndustrialMinimalSinPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicacionIndustrial
        fields = ('id', 'precio', 'precio_admon', 'tipo_negocio', 'bajo_precio', 'visitas')


class PublicacionLotesMinimalSinPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicacionLotes
        fields = ('id', 'precio', 'precio_admon', 'tipo_negocio', 'bajo_precio', 'visitas')


class ViviendaDetailSerializer(serializers.ModelSerializer):
  # fotografias_obj = FotografiaSerializer(source='fotografias', many=True, read_only=True)
    caracteristicas_obj = CaracteristicaSerializer(source='get_caracteristicas', many=True, read_only=True)
    agente = AgenteUserSerializer(read_only=True)
    publicacion_obj = PublicacionViviendaMinimalSinPropSerializer(source='get_publicacion', read_only=True)

    class Meta:
        model = Vivienda
        fields = (
            'id', 'habitaciones', 'banos', 'area_construida', 'area_privada', 'agente',
            'fotografias_obj', 'publicacion_obj', 'caracteristicas_obj', 'anio_construccion', 'estrato', 'descripcion',
            'direccion', 'tipo_vivienda', 'estacionamientos_totales', 'linkvirtual360', 'banos_sociales',
            'estacionamientos_cubiertos', 'estacionamientos_descubiertos', 'balcones', 'habitaciones_auxiliares',
            'terrazas', 'amoblado', 'estudios',
            'deposito', 'avaluo', 'coordenadas', 'municipio')


class ComercialDetailSerializer(serializers.ModelSerializer):
   # fotografias_obj = FotografiaSerializer(source='fotografias', many=True, read_only=True)
    caracteristicas_obj = CaracteristicaSerializer(source='get_caracteristicas', many=True, read_only=True)
    agente = AgenteUserSerializer(read_only=True)
    publicacion_obj = PublicacionComercialMinimalSinPropSerializer(source='get_publicacion_comercial', read_only=True)

    class Meta:
        model = Comercial
        fields = (
            'id', 'espacios', 'banos', 'area_construida', 'area_privada', 'agente',  'fotografias_obj',
            'publicacion_obj', 'caracteristicas_obj', 'anio_construccion', 'estrato', 'descripcion', 'direccion',
            'tipo', 'estacionamientos_totales', 'linkvirtual360',
            'estacionamientos_cubiertos', 'estacionamientos_descubiertos', 'balcones', 'terrazas', 'avaluo',
            'coordenadas', 'municipio')


class IndustrialDetailSerializer(serializers.ModelSerializer):
  #  fotografias_obj = FotografiaSerializer(source='fotografias', many=True, read_only=True)
    caracteristicas_obj = CaracteristicaSerializer(source='get_caracteristicas', many=True, read_only=True)
    agente = AgenteUserSerializer(read_only=True)
    publicacion_obj = PublicacionIndustrialMinimalSinPropSerializer(source='get_publicacion_industrial', read_only=True)

    class Meta:
        model = Industrial
        fields = (
            'id', 'espacios', 'banos', 'area_construida', 'area_privada', 'agente',  'fotografias_obj',
            'publicacion_obj', 'caracteristicas_obj', 'anio_construccion', 'descripcion', 'direccion',
            'tipo', 'linkvirtual360', 'avaluo', 'coordenadas', 'municipio')


class LotesDetailSerializer(serializers.ModelSerializer):
  #  fotografias_obj = FotografiaSerializer(source='fotografias', many=True, read_only=True)
    caracteristicas_obj = CaracteristicaSerializer(source='get_caracteristicas', many=True, read_only=True)
    agente = AgenteUserSerializer(read_only=True)
    publicacion_obj = PublicacionLotesMinimalSinPropSerializer(source='get_publicacion_lotes', read_only=True)

    class Meta:
        model = Lotes
        fields = (
            'id', 'area_lote', 'area_lote', 'agente',  'fotografias_obj',
            'publicacion_obj', 'caracteristicas_obj', 'descripcion', 'direccion',
            'tipo', 'linkvirtual360', 'avaluo', 'coordenadas', 'municipio')


class PropiedadGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propiedad

    def to_representation(self, obj):
        """
        Because Propiedad is Polymorphic
        """
        if isinstance(obj, Vivienda):
            return ViviendaSerializer(obj, context=self.context).to_representation(obj)
        if isinstance(obj, Comercial):
            return ComercialSerializer(obj, context=self.context).to_representation(obj)
        if isinstance(obj, Industrial):
            return IndustrialSerializer(obj, context=self.context).to_representation(obj)
        if isinstance(obj, Lotes):
            return LotesSerializer(obj, context=self.context).to_representation(obj)
        return super(PropiedadGETSerializer, self).to_representation(obj)
