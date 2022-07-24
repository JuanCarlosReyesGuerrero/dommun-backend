from django.urls import path

from agentes.views import AgentesList, GestionDocumentalList, AgentesRetrive, AgentesDetail

urlpatterns = [
    path('agentes/', AgentesList.as_view()),
    path('gestiondocumental/', GestionDocumentalList.as_view()),
    #path(r'^(?P<slug>[-\w]+)/$', AgentesRetrive.as_view({'get': 'retrieve'}, lookup_field='slug')),
    #path(r'^agente/(?P<pk>\w+)/$', AgentesDetail.as_view()),
]
