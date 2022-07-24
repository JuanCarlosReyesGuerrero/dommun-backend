from django.contrib import admin

from publicaciones.models import PublicacionVivienda, PublicacionComercial, PublicacionIndustrial, PublicacionLotes

admin.site.register(PublicacionVivienda)
admin.site.register(PublicacionComercial)
admin.site.register(PublicacionIndustrial)
admin.site.register(PublicacionLotes)
