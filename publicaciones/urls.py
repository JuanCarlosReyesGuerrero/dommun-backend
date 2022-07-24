from django.conf.urls import url

from publicaciones import views

urlpatterns = [
    url(r'^vivienda/$', views.PublicacionViviendaList.as_view()),
    url(r'^vivienda/(?P<pk>[0-9]+)/$', views.PublicacionViviendaDetail.as_view()),
    url(r'^comercial/$', views.PublicacionComercialList.as_view()),
    url(r'^comercial/(?P<pk>[0-9]+)/$', views.PublicacionComercialDetail.as_view()),
    url(r'^industrial/$', views.PublicacionIndustrialList.as_view()),
    url(r'^industrial/(?P<pk>[0-9]+)/$', views.PublicacionIndustrialDetail.as_view()),
    url(r'^lotes/$', views.PublicacionLotesList.as_view()),
    url(r'^lotes/(?P<pk>[0-9]+)/$', views.PublicacionLotesDetail.as_view()),
    url(r'^avaluoenlinea/$', views.avaluoenlinea),
]
