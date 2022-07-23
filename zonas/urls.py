from django.urls import path

from zonas.views import ZonaList, DepartamentoList, MunicipioList, ZonaDetail

urlpatterns = [
    path('zona/', ZonaList.as_view()),
    path('departamento/', DepartamentoList.as_view()),
    path('municipio/', MunicipioList.as_view()),
    path(r'^(?P<pk>\w+)/$', ZonaDetail.as_view()),
]