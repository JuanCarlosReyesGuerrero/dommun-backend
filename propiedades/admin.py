from django.contrib import admin

from propiedades.models import Vivienda, Comercial, Industrial, Lotes, Caracteristica, Fotografia, DocumentoPropiedad, \
    TipoDocumentoPropiedad

admin.site.register(Vivienda)
admin.site.register(Comercial)
admin.site.register(Industrial)
admin.site.register(Lotes)
admin.site.register(Caracteristica)
admin.site.register(Fotografia)
admin.site.register(DocumentoPropiedad)
admin.site.register(TipoDocumentoPropiedad)