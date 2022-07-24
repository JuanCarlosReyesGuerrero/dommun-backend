import hashlib

import django_filters
from django.contrib.gis.measure import D
from django.core.cache import cache
from django.core.mail import EmailMessage
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import authentication

from rest_framework.decorators import api_view

import requests
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

# *****************************************
#   Clase filtro publicación vivienda
# *****************************************
from publicaciones.models import PublicacionVivienda, PublicacionComercial, PublicacionLotes, PublicacionIndustrial, \
    Publicacion
from publicaciones.serializers import PublicacionGETSerializer, PublicacionViviendaSerializer, \
    PublicacionViviendaMinimalSerializer, PublicacionComercialSerializer, PublicacionIndustrialSerializer, \
    PublicacionLotesSerializer, PublicacionGETSerializerLotes, PublicacionLotesMinimalSerializer, \
    PublicacionGETSerializerComercial, PublicacionComercialMinimalSerializer, PublicacionGETSerializerIndustrial, \
    PublicacionIndustrialMinimalSerializer
from zonas.models import Zona


class PublicacionViviendaFilter(django_filters.FilterSet):
    tipo_negocio = django_filters.CharFilter(name="tipo_negocio")
    precio_min = django_filters.NumberFilter(name="precio", lookup_type='gte')
    precio_max = django_filters.NumberFilter(name="precio", lookup_type='lte')
    area_min = django_filters.NumberFilter(name="propiedad__area_construida", lookup_type='gte')
    area_max = django_filters.NumberFilter(name="propiedad__area_construida", lookup_type='lte')
    estrato_min = django_filters.NumberFilter(name="propiedad__estrato", lookup_type='gte')
    estrato_max = django_filters.NumberFilter(name="propiedad__estrato", lookup_type='lte')
    habitaciones_min = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='gte')
    habitaciones_max = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='lte')
    habitaciones = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='gte')
    banos_min = django_filters.NumberFilter(name="propiedad__banos", lookup_type='gte')
    banos_max = django_filters.NumberFilter(name="propiedad__banos", lookup_type='lte')
    banos = django_filters.NumberFilter(name="propiedad__banos", lookup_type='gte')
    garajes_min = django_filters.NumberFilter(name="propiedad__estacionamientos_cubiertos", lookup_type='gte')
    garajes_max = django_filters.NumberFilter(name="propiedad__estacionamientos_cubiertos", lookup_type='lte')
    garajes = django_filters.NumberFilter(name="propiedad__estacionamientos", lookup_type='gte')
    antiguedad_max = django_filters.NumberFilter(name="propiedad__antiguedad", lookup_type='lte')
    # zona = django_filters.MethodFilter(action='inmuebles_zona')
    # radio = django_filters.MethodFilter(action='inmuebles_radio')
    agente = django_filters.NumberFilter(name="agente")
    propietario = django_filters.NumberFilter(name="propiedad__propietario")
    estado = django_filters.NumberFilter(name="estado")
    es_exclusivo = django_filters.BooleanFilter()
    # zonas_appto = django_filters.MethodFilter(action='inmuebles_zona_resultado')
    balcones_min = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='gte')
    balcones_max = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='lte')
    balcones = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='gte')
    habitaciones_auxiliares_min = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares",
                                                              lookup_type='gte')
    habitaciones_auxiliares_max = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares",
                                                              lookup_type='lte')
    habitaciones_auxiliares = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares", lookup_type='gte')
    terrazas_min = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='gte')
    terrazas_max = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='lte')
    terrazas = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='gte')
    bajo_precio = django_filters.BooleanFilter()
    propiedad = django_filters.NumberFilter(name="propiedad")
    id = django_filters.NumberFilter(name="id")

    class Meta:
        model = PublicacionVivienda
        fields = ['tipo_negocio', 'precio_min', 'precio_max', 'area_min', 'area_max', 'estrato_min', 'estrato_max',
                  'habitaciones_min', 'habitaciones_max', 'habitaciones', 'banos_min', 'banos_max', 'banos',
                  'garajes_min', 'garajes_max', 'garajes', 'antiguedad_max', 'agente', 'propietario',
                  'estado', 'es_exclusivo', 'balcones_min', 'balcones_max', 'balcones',
                  'habitaciones_auxiliares_min', 'habitaciones_auxiliares_max', 'habitaciones_auxiliares',
                  'terrazas_min', 'terrazas_max', 'terrazas', 'bajo_precio', 'propiedad']


# *****************************************
#   Clase filtro publicación comercial
# *****************************************
class PublicacionComercialFilter(django_filters.FilterSet):
    tipo_negocio = django_filters.CharFilter(name="tipo_negocio")
    precio_min = django_filters.NumberFilter(name="precio", lookup_type='gte')
    precio_max = django_filters.NumberFilter(name="precio", lookup_type='lte')
    area_min = django_filters.NumberFilter(name="propiedad__area_construida", lookup_type='gte')
    area_max = django_filters.NumberFilter(name="propiedad__area_construida", lookup_type='lte')
    estrato_min = django_filters.NumberFilter(name="propiedad__estrato", lookup_type='gte')
    estrato_max = django_filters.NumberFilter(name="propiedad__estrato", lookup_type='lte')
    habitaciones_min = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='gte')
    habitaciones_max = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='lte')
    habitaciones = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='gte')
    banos_min = django_filters.NumberFilter(name="propiedad__banos", lookup_type='gte')
    banos_max = django_filters.NumberFilter(name="propiedad__banos", lookup_type='lte')
    banos = django_filters.NumberFilter(name="propiedad__banos", lookup_type='gte')
    garajes_min = django_filters.NumberFilter(name="propiedad__estacionamientos_cubiertos", lookup_type='gte')
    garajes_max = django_filters.NumberFilter(name="propiedad__estacionamientos_cubiertos", lookup_type='lte')
    garajes = django_filters.NumberFilter(name="propiedad__estacionamientos", lookup_type='gte')
    antiguedad_max = django_filters.NumberFilter(name="propiedad__antiguedad", lookup_type='lte')
    # zona = django_filters.MethodFilter(action='inmuebles_zona')
    # radio = django_filters.MethodFilter(action='inmuebles_radio')
    agente = django_filters.NumberFilter(name="agente")
    propietario = django_filters.NumberFilter(name="propiedad__propietario")
    estado = django_filters.NumberFilter(name="estado")
    es_exclusivo = django_filters.BooleanFilter()
    # zonas_appto = django_filters.MethodFilter(action='inmuebles_zona_resultado')
    balcones_min = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='gte')
    balcones_max = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='lte')
    balcones = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='gte')
    habitaciones_auxiliares_min = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares",
                                                              lookup_type='gte')
    habitaciones_auxiliares_max = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares",
                                                              lookup_type='lte')
    habitaciones_auxiliares = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares", lookup_type='gte')
    terrazas_min = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='gte')
    terrazas_max = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='lte')
    terrazas = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='gte')
    bajo_precio = django_filters.BooleanFilter()
    propiedad = django_filters.NumberFilter(name="propiedad")

    class Meta:
        model = PublicacionComercial
        fields = ['tipo_negocio', 'precio_min', 'precio_max', 'area_min', 'area_max', 'estrato_min', 'estrato_max',
                  'habitaciones_min', 'habitaciones_max', 'habitaciones', 'banos_min', 'banos_max', 'banos',
                  'garajes_min', 'garajes_max', 'garajes', 'antiguedad_max', 'agente', 'propietario',
                  'estado', 'es_exclusivo', 'balcones_min', 'balcones_max', 'balcones',
                  'habitaciones_auxiliares_min', 'habitaciones_auxiliares_max', 'habitaciones_auxiliares',
                  'terrazas_min', 'terrazas_max', 'terrazas', 'bajo_precio']


# *****************************************
#   Clase filtro publicación lotes
# *****************************************
class PublicacionLotesFilter(django_filters.FilterSet):
    tipo_negocio = django_filters.CharFilter(name="tipo_negocio")
    precio_min = django_filters.NumberFilter(name="precio", lookup_type='gte')
    precio_max = django_filters.NumberFilter(name="precio", lookup_type='lte')
    area_min = django_filters.NumberFilter(name="propiedad__area_construida", lookup_type='gte')
    area_max = django_filters.NumberFilter(name="propiedad__area_construida", lookup_type='lte')
    estrato_min = django_filters.NumberFilter(name="propiedad__estrato", lookup_type='gte')
    estrato_max = django_filters.NumberFilter(name="propiedad__estrato", lookup_type='lte')
    habitaciones_min = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='gte')
    habitaciones_max = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='lte')
    habitaciones = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='gte')
    banos_min = django_filters.NumberFilter(name="propiedad__banos", lookup_type='gte')
    banos_max = django_filters.NumberFilter(name="propiedad__banos", lookup_type='lte')
    banos = django_filters.NumberFilter(name="propiedad__banos", lookup_type='gte')
    garajes_min = django_filters.NumberFilter(name="propiedad__estacionamientos_cubiertos", lookup_type='gte')
    garajes_max = django_filters.NumberFilter(name="propiedad__estacionamientos_cubiertos", lookup_type='lte')
    garajes = django_filters.NumberFilter(name="propiedad__estacionamientos", lookup_type='gte')
    antiguedad_max = django_filters.NumberFilter(name="propiedad__antiguedad", lookup_type='lte')
    # zona = django_filters.MethodFilter(action='inmuebles_zona')
    # radio = django_filters.MethodFilter(action='inmuebles_radio')
    agente = django_filters.NumberFilter(name="agente")
    propietario = django_filters.NumberFilter(name="propiedad__propietario")
    estado = django_filters.NumberFilter(name="estado")
    es_exclusivo = django_filters.BooleanFilter()
    # zonas_appto = django_filters.MethodFilter(action='inmuebles_zona_resultado')
    balcones_min = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='gte')
    balcones_max = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='lte')
    balcones = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='gte')
    habitaciones_auxiliares_min = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares",
                                                              lookup_type='gte')
    habitaciones_auxiliares_max = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares",
                                                              lookup_type='lte')
    habitaciones_auxiliares = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares", lookup_type='gte')
    terrazas_min = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='gte')
    terrazas_max = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='lte')
    terrazas = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='gte')
    bajo_precio = django_filters.BooleanFilter()
    propiedad = django_filters.NumberFilter(name="propiedad")

    class Meta:
        model = PublicacionLotes
        fields = ['tipo_negocio', 'precio_min', 'precio_max', 'area_min', 'area_max', 'estrato_min', 'estrato_max',
                  'habitaciones_min', 'habitaciones_max', 'habitaciones', 'banos_min', 'banos_max', 'banos',
                  'garajes_min', 'garajes_max', 'garajes', 'antiguedad_max', 'agente', 'propietario',
                  'estado', 'es_exclusivo', 'balcones_min', 'balcones_max', 'balcones',
                  'habitaciones_auxiliares_min', 'habitaciones_auxiliares_max', 'habitaciones_auxiliares',
                  'terrazas_min', 'terrazas_max', 'terrazas', 'bajo_precio']


# *****************************************
#   Clase filtro publicación industrial
# *****************************************
class PublicacionIndustrialFilter(django_filters.FilterSet):
    tipo_negocio = django_filters.CharFilter(name="tipo_negocio")
    precio_min = django_filters.NumberFilter(name="precio", lookup_type='gte')
    precio_max = django_filters.NumberFilter(name="precio", lookup_type='lte')
    area_min = django_filters.NumberFilter(name="propiedad__area_construida", lookup_type='gte')
    area_max = django_filters.NumberFilter(name="propiedad__area_construida", lookup_type='lte')
    estrato_min = django_filters.NumberFilter(name="propiedad__estrato", lookup_type='gte')
    estrato_max = django_filters.NumberFilter(name="propiedad__estrato", lookup_type='lte')
    habitaciones_min = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='gte')
    habitaciones_max = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='lte')
    habitaciones = django_filters.NumberFilter(name="propiedad__habitaciones", lookup_type='gte')
    banos_min = django_filters.NumberFilter(name="propiedad__banos", lookup_type='gte')
    banos_max = django_filters.NumberFilter(name="propiedad__banos", lookup_type='lte')
    banos = django_filters.NumberFilter(name="propiedad__banos", lookup_type='gte')
    garajes_min = django_filters.NumberFilter(name="propiedad__estacionamientos_cubiertos", lookup_type='gte')
    garajes_max = django_filters.NumberFilter(name="propiedad__estacionamientos_cubiertos", lookup_type='lte')
    garajes = django_filters.NumberFilter(name="propiedad__estacionamientos", lookup_type='gte')
    antiguedad_max = django_filters.NumberFilter(name="propiedad__antiguedad", lookup_type='lte')
    # zona = django_filters.MethodFilter(action='inmuebles_zona')
    # radio = django_filters.MethodFilter(action='inmuebles_radio')
    agente = django_filters.NumberFilter(name="agente")
    propietario = django_filters.NumberFilter(name="propiedad__propietario")
    estado = django_filters.NumberFilter(name="estado")
    es_exclusivo = django_filters.BooleanFilter()
    # zonas_appto = django_filters.MethodFilter(action='inmuebles_zona_resultado')
    balcones_min = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='gte')
    balcones_max = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='lte')
    balcones = django_filters.NumberFilter(name="propiedad__balcones", lookup_type='gte')
    habitaciones_auxiliares_min = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares",
                                                              lookup_type='gte')
    habitaciones_auxiliares_max = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares",
                                                              lookup_type='lte')
    habitaciones_auxiliares = django_filters.NumberFilter(name="propiedad__habitaciones_auxiliares", lookup_type='gte')
    terrazas_min = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='gte')
    terrazas_max = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='lte')
    terrazas = django_filters.NumberFilter(name="propiedad__terrazas", lookup_type='gte')
    bajo_precio = django_filters.BooleanFilter()
    propiedad = django_filters.NumberFilter(name="propiedad")

    class Meta:
        model = PublicacionIndustrial
        fields = ['tipo_negocio', 'precio_min', 'precio_max', 'area_min', 'area_max', 'estrato_min', 'estrato_max',
                  'habitaciones_min', 'habitaciones_max', 'habitaciones', 'banos_min', 'banos_max', 'banos',
                  'garajes_min', 'garajes_max', 'garajes', 'antiguedad_max', 'agente', 'propietario',
                  'estado', 'es_exclusivo', 'balcones_min', 'balcones_max', 'balcones',
                  'habitaciones_auxiliares_min', 'habitaciones_auxiliares_max', 'habitaciones_auxiliares',
                  'terrazas_min', 'terrazas_max', 'terrazas', 'bajo_precio']


# **********************************************
#   Clase publicación vivienda lista
# **********************************************
class PublicacionViviendaList(generics.ListCreateAPIView):
    serializer_class = PublicacionVivienda
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = PublicacionViviendaFilter
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def get_queryset(self):
        qs = PublicacionVivienda.objects.all()
        return qs


# **********************************************
#   Clase publicación vivienda detalle
# **********************************************
class PublicacionViviendaDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                                GenericAPIView, ):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionViviendaSerializer
    parser_classes = JSONParser, MultiPartParser
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        inm = self.get_object()
        user = request.user
        if self.request.user.is_authenticated():
            ser = PublicacionViviendaSerializer(inm)
        else:
            ser = PublicacionViviendaSerializer(inm)
        return Response(ser.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #      return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        propiedadPatch = self.partial_update(request, *args, **kwargs)

        publicacion2 = PublicacionVivienda.objects.get(id=self.request.data['id'])

        if publicacion2.estado == 3:
            email = EmailMessage('Tienes una publicación actualizada',
                                 'Tienes una publicación actualizada para portales, código: ' + str(
                                     publicacion2.propiedad_id) + ' - Agente: ' + str(publicacion2.agente),
                                 to=['contenido@appto.co'])
            email.send()
        else:
            email = EmailMessage('Tienes una publicación despublicada',
                                 'Tienes una publicación despublicada para portales, código: ' + str(
                                     publicacion2.propiedad_id) + ' - Agente: ' + str(publicacion2.agente),
                                 to=['contenido@appto.co'])
            email.send()

        # return self.partial_update(request, *args, **kwargs)
        return propiedadPatch


# **********************************************
#   Clase publicación comercial detalle
# **********************************************
class PublicacionComercialDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                                 GenericAPIView, ):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionComercialSerializer
    parser_classes = JSONParser, MultiPartParser
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        inm = self.get_object()
        user = request.user
        if self.request.user.is_authenticated():
            ser = PublicacionComercialSerializer(inm)
        else:
            ser = PublicacionComercialSerializer(inm)
        return Response(ser.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #      return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        propiedadPatch = self.partial_update(request, *args, **kwargs)

        publicacion2 = PublicacionComercial.objects.get(id=self.request.data['id'])

        if publicacion2.estado == 3:
            email = EmailMessage('Tienes una publicación actualizada',
                                 'Tienes una publicación actualizada para portales, código: ' + str(
                                     publicacion2.propiedad_id) + ' - Agente: ' + str(publicacion2.agente),
                                 to=['contenido@appto.co'])
            email.send()
        else:
            email = EmailMessage('Tienes una publicación despublicada',
                                 'Tienes una publicación despublicada para portales, código: ' + str(
                                     publicacion2.propiedad_id) + ' - Agente: ' + str(publicacion2.agente),
                                 to=['contenido@appto.co'])
            email.send()

        # return self.partial_update(request, *args, **kwargs)
        return propiedadPatch


# **********************************************
#   Clase publicación industrial detalle
# **********************************************
class PublicacionIndustrialDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                                  GenericAPIView, ):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionIndustrialSerializer
    parser_classes = JSONParser, MultiPartParser
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        inm = self.get_object()
        user = request.user
        if self.request.user.is_authenticated():
            ser = PublicacionIndustrialSerializer(inm)
        else:
            ser = PublicacionIndustrialSerializer(inm)
        return Response(ser.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #      return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        propiedadPatch = self.partial_update(request, *args, **kwargs)

        publicacion2 = PublicacionIndustrial.objects.get(id=self.request.data['id'])

        if publicacion2.estado == 3:
            email = EmailMessage('Tienes una publicación actualizada',
                                 'Tienes una publicación actualizada para portales, código: ' + str(
                                     publicacion2.propiedad_id) + ' - Agente: ' + str(publicacion2.agente),
                                 to=['contenido@appto.co'])
            email.send()
        else:
            email = EmailMessage('Tienes una publicación despublicada',
                                 'Tienes una publicación despublicada para portales, código: ' + str(
                                     publicacion2.propiedad_id) + ' - Agente: ' + str(publicacion2.agente),
                                 to=['contenido@appto.co'])
            email.send()

        # return self.partial_update(request, *args, **kwargs)
        return propiedadPatch


# **********************************************
#   Clase publicación lotes detalle
# **********************************************
class PublicacionLotesDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                             GenericAPIView, ):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionLotesSerializer
    parser_classes = JSONParser, MultiPartParser
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        inm = self.get_object()
        user = request.user
        if self.request.user.is_authenticated():
            ser = PublicacionLotesSerializer(inm)
        else:
            ser = PublicacionLotesSerializer(inm)
        return Response(ser.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #      return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        propiedadPatch = self.partial_update(request, *args, **kwargs)

        publicacion2 = PublicacionLotes.objects.get(id=self.request.data['id'])

        if publicacion2.estado == 3:
            email = EmailMessage('Tienes una publicación actualizada',
                                 'Tienes una publicación actualizada para portales, código: ' + str(
                                     publicacion2.propiedad_id) + ' - Agente: ' + str(publicacion2.agente),
                                 to=['contenido@appto.co'])
            email.send()
        else:
            email = EmailMessage('Tienes una publicación despublicada',
                                 'Tienes una publicación despublicada para portales, código: ' + str(
                                     publicacion2.propiedad_id) + ' - Agente: ' + str(publicacion2.agente),
                                 to=['contenido@appto.co'])
            email.send()

        # return self.partial_update(request, *args, **kwargs)
        return propiedadPatch


# **********************************************
#   Clase publicación lotes lista
# **********************************************
class PublicacionLotesList(generics.ListCreateAPIView):
    serializer_class = PublicacionLotes
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = PublicacionLotesFilter
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.ordering_fields = ('fecha_creacion', 'precio',)
        m = hashlib.md5()
        m.update(str(json.dumps(request.query_params)).encode('utf-8'))
        cache_key = 'inmuebles_lotes_maplist_t_' + m.hexdigest()
        cache_time = 600
        if self.request.user.is_authenticated():
            cache_key = str(user.id) + 'inmuebles_lotes_maplist_t_' + m.hexdigest()
            cache_time = 30
            # time to live in seconds
        qs = cache.get(cache_key)
        rep = None
        if user.is_staff or not qs:
            rep = self.list(request, *args, **kwargs)
            qs = json.dumps(rep.data)
            cache.set(cache_key, qs, cache_time)
        else:
            rep = Response(json.loads(qs))
        return rep

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_authenticated():

            self.serializer_class = PublicacionGETSerializerLotes
            return PublicacionLotes.objects.all()
        else:
            self.serializer_class = PublicacionLotesMinimalSerializer
            return PublicacionLotes.objects.filter(estado=PublicacionLotes.ESTADO_PUBLICADO)


# **********************************************
#   Clase publicación comercial lista
# **********************************************
class PublicacionComercialList(generics.ListCreateAPIView):
    serializer_class = PublicacionComercial
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = PublicacionComercialFilter
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.ordering_fields = ('fecha_creacion', 'precio',)
        m = hashlib.md5()
        m.update(str(json.dumps(request.query_params)).encode('utf-8'))
        cache_key = 'inmuebles_comercial_maplist_t_' + m.hexdigest()
        cache_time = 600
        if self.request.user.is_authenticated():
            cache_key = str(user.id) + 'inmuebles_comercial_maplist_t_' + m.hexdigest()
            cache_time = 30
            # time to live in seconds
        qs = cache.get(cache_key)
        rep = None
        if user.is_staff or not qs:
            rep = self.list(request, *args, **kwargs)
            qs = json.dumps(rep.data)
            cache.set(cache_key, qs, cache_time)
        else:
            rep = Response(json.loads(qs))
        return rep

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_authenticated():
            # self.serializer_class = PublicacionGETSerializerComercial
            self.serializer_class = PublicacionGETSerializerComercial
            return PublicacionComercial.objects.all()
        else:
            self.serializer_class = PublicacionComercialMinimalSerializer
            return PublicacionComercial.objects.filter(estado=PublicacionComercial.ESTADO_PUBLICADO)

    def post(self, request, *args, **kwargs):
        self.serializer_class = PublicacionComercialSerializer

        propiedadCreate = self.create(request, *args, **kwargs)

        email = EmailMessage('Tienes una nueva publicación',
                             'Tienes una nueva publicación para portales, código: ' + str(
                                 self.request.data['propiedad']) + ' - Agente: ' + str(
                                 propiedadCreate.data['agente_obj']['nombre']) + ' ' +
                             str(propiedadCreate.data['agente_obj']['apellido']),
                             to=['contenido@appto.co'])
        email.send()

        # return self.create(request, *args, **kwargs)
        return propiedadCreate


# **********************************************
#   Clase publicación industrial lista
# **********************************************
class PublicacionIndustrialList(generics.ListCreateAPIView):
    serializer_class = PublicacionIndustrial
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = PublicacionIndustrialFilter
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.ordering_fields = ('fecha_creacion', 'precio',)
        m = hashlib.md5()
        m.update(str(json.dumps(request.query_params)).encode('utf-8'))
        cache_key = 'inmuebles_Industrial_maplist_t_' + m.hexdigest()
        cache_time = 600
        if self.request.user.is_authenticated():
            cache_key = str(user.id) + 'inmuebles_Industrial_maplist_t_' + m.hexdigest()
            cache_time = 30
            # time to live in seconds
        qs = cache.get(cache_key)
        rep = None
        if user.is_staff or not qs:
            rep = self.list(request, *args, **kwargs)
            qs = json.dumps(rep.data)
            cache.set(cache_key, qs, cache_time)
        else:
            rep = Response(json.loads(qs))
        return rep

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_authenticated():
            self.serializer_class = PublicacionGETSerializerIndustrial
            return PublicacionIndustrial.objects.all()
        else:
            self.serializer_class = PublicacionIndustrialMinimalSerializer
            return PublicacionIndustrial.objects.filter(estado=PublicacionIndustrial.ESTADO_PUBLICADO)

    def post(self, request, *args, **kwargs):
        self.serializer_class = PublicacionIndustrialSerializer

        propiedadCreate = self.create(request, *args, **kwargs)

        email = EmailMessage('Tienes una nueva publicación',
                             'Tienes una nueva publicación para portales, código: ' + str(
                                 self.request.data['propiedad']) + ' - Agente: ' + str(
                                 propiedadCreate.data['agente_obj']['nombre']) + ' ' +
                             str(propiedadCreate.data['agente_obj']['apellido']),
                             to=['contenido@appto.co'])
        email.send()

        # return self.create(request, *args, **kwargs)
        return propiedadCreate


# **********************************************
#   Clase avaluo en linea
# **********************************************
@csrf_exempt
@api_view(['POST'])
def avaluoenlinea(request):
    if request.method == 'POST':
        try:
            url = 'https://api.avaluoenlinea.com/servicios/API_call'
            data = JSONParser().parse(request)
            headers = {'Content-Type': 'application/json', 'x-api-key': 'Pb5NOARRrr2v2jN9ENkKF2zKoHLeDpMY4mLt6zux'}

            r = requests.post(url, data=json.dumps(data), headers=headers).json()

            return Response(r)

        except Exception as e:
            return HttpResponse("%s." % e)
