from django.contrib import admin

from leads.models import Consignacion, Administracion, PromotorCandidato, ContactoPagina, ContactoPortales, \
    ContactoCurso, ContactoCita

admin.site.register(Consignacion)

admin.site.register(Administracion)

admin.site.register(PromotorCandidato)

admin.site.register(ContactoPagina)

admin.site.register(ContactoPortales)

admin.site.register(ContactoCurso)

admin.site.register(ContactoCita)
