from rest_framework import generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination

from agentes.models import Agente, GestionDocumental
from agentes.serializers import AgenteLiteSerializer, AgenteSerializer, AgentePATCHSerializer, \
    GestionDocumentalSerializer


class AgentesList(generics.ListCreateAPIView):
    queryset = Agente.objects.exclude(foto_perfil='').filter(activo=True, publicado=True, foto_perfil__isnull=False)
    serializer_class = AgenteLiteSerializer

    def get_queryset(self):
        qs = Agente.objects.all()
        return qs


class AgentesDetail(generics.RetrieveUpdateAPIView):
    queryset = Agente.objects.exclude(foto_perfil='').filter(activo=True, publicado=True, foto_perfil__isnull=False)
    serializer_class = AgenteSerializer

    def patch(self, request, *args, **kwargs):
        self.serializer_class = AgentePATCHSerializer
        return self.partial_update(request, *args, **kwargs)


class AgentesRetrive(viewsets.ReadOnlyModelViewSet):
    queryset = Agente.objects.exclude(foto_perfil='').filter(activo=True, publicado=True, foto_perfil__isnull=False)
    serializer_class = AgenteSerializer


# *************************************************
# Clase paginación Gestión documental
# *************************************************
class GestionDocumentalSetPagination(PageNumberPagination):
    page_size = 18
    page_size_query_param = 'page_size'
    max_page_size = 30


# *************************************************
# Clase Gestión documental
# *************************************************
class GestionDocumentalList(generics.ListAPIView):
    queryset = GestionDocumental.objects.none()
    serializer_class = GestionDocumentalSerializer
    pagination_class = GestionDocumentalSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['nombre']

    def get_queryset(self):
        qs = GestionDocumental.objects.all()
        return qs