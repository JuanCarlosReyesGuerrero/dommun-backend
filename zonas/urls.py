from django.urls import path

from zonas.views import ZonaList, DepartamentoList, MunicipioList, ZonaDetail

urlpatterns = [
    path('zonas/', ZonaList.as_view()),
    path('departamentos/', DepartamentoList.as_view()),
    path('municipios/', MunicipioList.as_view()),
    #path(r'^(?P<pk>\w+)/$', ZonaDetail.as_view()),
]
