from django.contrib import admin

from clientes.models import Cliente, Necesidad, PropiedadNecesidad

admin.site.register(Cliente)
admin.site.register(Necesidad)
admin.site.register(PropiedadNecesidad)
