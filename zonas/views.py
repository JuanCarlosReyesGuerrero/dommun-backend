import django_filters

from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.response import Response

from zonas.models import Departamento, Zona, Municipio
from zonas.serializers import ZonaLiteSerializer, ZonaSerializer, DepartamentoSerializer, MunicipioSerializer


class ZonaFilter(django_filters.FilterSet):
    class Meta:
        model = Zona
        fields = ['tipo_zona']

    def tipo_zona(self, queryset, value):
        zonas = queryset.objects.filter(tipo_zona__id=value)
        return zonas


class ZonaList(generics.ListAPIView):
    serializer_class = ZonaLiteSerializer
    filter_class = ZonaFilter
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def get_queryset(self):
        qs = Zona.objects.all()
        return qs

    def list(self, request):
        cache_key = 'zona_lista'
        cache_time = 3600  # time to live in seconds
        qs = cache.get(cache_key)
        if not qs:
            queryset = self.get_queryset()
            serializer = ZonaLiteSerializer(queryset, many=True)
            qs = serializer.data
            cache.set(cache_key, qs, cache_time)
        return Response(qs)


class ZonaDetail(generics.RetrieveAPIView):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer


class DepartamentoList(generics.ListAPIView):
    serializer_class = DepartamentoSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def get_queryset(self):
        qs = Departamento.objects.all()
        return qs


class MunicipioList(generics.ListAPIView):
    serializer_class = MunicipioSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def get_queryset(self):
        qs = Municipio.objects.all()
        return qs
