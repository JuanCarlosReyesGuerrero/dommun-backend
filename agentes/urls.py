from django.conf.urls import url

from agentes.views import AgentesList, GestionDocumentalList, AgentesRetrive, AgentesDetail

urlpatterns = [
    url(r'^$', AgentesList.as_view()),
    url(r'^gestiondocumental/$', GestionDocumentalList.as_view()),
    url(r'^(?P<slug>[-\w]+)/$', AgentesRetrive.as_view({'get': 'retrieve'}, lookup_field='slug')),
    url(r'^agente/(?P<pk>\w+)/$', AgentesDetail.as_view()),
]
