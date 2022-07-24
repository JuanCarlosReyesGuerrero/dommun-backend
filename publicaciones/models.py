from django.db import models
from polymorphic.models import PolymorphicModel

from agentes.models import Agente
from propiedades.models import Vivienda, Comercial, Industrial, Lotes


def upload_docs_propiedad(instance, filename):
    import os
    import random
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    return 'documentos/' + str(instance.propiedad.id) + '/%s%s' % (
        now().strftime("%Y%m%d%H%M%S") + "" + str(random.randint(1, 1000000)),
        filename_ext.lower(),
    )


class Publicacion(PolymorphicModel):
    TIPOS_URGENCIA = (
        ('PPP', 'PPP'),
        ('PP', 'PP'),
        ('P', 'P'),
    )

    tipo_urgencia = models.CharField(max_length=32, choices=TIPOS_URGENCIA, default='P')

    agente = models.ForeignKey(Agente, related_name='publicaciones', limit_choices_to={'activo': True}, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    ESTADO_CREADO = 1
    ESTADO_VALIDACION = 0
    ESTADO_PUBLICACION_NO_CUMPLE = 2
    ESTADO_PUBLICADO = 3
    ESTADO_CERRADO_CON_DOMMUN = 4
    ESTADO_EL_CLIENTE_SE_ARREPINTIO = 5
    ESTADO_EL_CLIENTE_VENDIO_POR_OTRO_MEDIO = 6
    ESTADO_BROKER_DECIDE_NO_CONTINUAR = 7
    ESTADO_CLIENTE_NO_APARECE = 8
    ESTADO_CLIENTE_PIDE_CAMBIO_BROKER = 9
    ESTADO_DUPLICADO = 10
    ESTADO_DESPUBLICADO = 11

    ESTADOS = (
        (ESTADO_CREADO, 'En Validación Fotos'),
        (ESTADO_VALIDACION, 'En proceso SAB'),
        (ESTADO_PUBLICACION_NO_CUMPLE, 'Publicación NO CUMPLE'),
        (ESTADO_PUBLICADO, 'Publicado'),
        (ESTADO_CERRADO_CON_DOMMUN, 'Cerrado con Dommun'),
        (ESTADO_EL_CLIENTE_SE_ARREPINTIO, 'El cliente se arrepintió'),
        (ESTADO_EL_CLIENTE_VENDIO_POR_OTRO_MEDIO, 'El cliente cerró por otro medio'),
        (ESTADO_BROKER_DECIDE_NO_CONTINUAR, 'El broker decide no continuar'),
        (ESTADO_CLIENTE_NO_APARECE, 'Cliente no aparece'),
        (ESTADO_CLIENTE_PIDE_CAMBIO_BROKER, 'Cliente pide cambio de broker'),
        (ESTADO_DUPLICADO, 'Duplicado'),
        (ESTADO_DESPUBLICADO, 'Despublicado')
    )

    estado = models.IntegerField(null=False, choices=ESTADOS, default=ESTADO_PUBLICADO)

    razon = models.TextField(null=True, blank=True)

    publicacion_relacionada = models.ForeignKey('self', related_name='relacionada', null=True, blank=True, on_delete=models.CASCADE)

    precio = models.DecimalField(max_digits=17, decimal_places=2, null=False, blank=False)
    precio_admon = models.DecimalField(max_digits=17, decimal_places=2, null=False, blank=False)

    es_exclusivo = models.BooleanField(null=False, default=False)

    certificado_lib_trad = models.FileField(upload_to=upload_docs_propiedad, blank=True, null=True)
    contrato = models.FileField(upload_to=upload_docs_propiedad, blank=True, null=True)

    publicado_portales = models.BooleanField(null=False, default=False)

    confirmo_motivo = models.BooleanField(null=False, default=False)

    bajo_precio = models.BooleanField(null=False, default=False)
    visitas = models.IntegerField(null=True, blank=True, default=0)

    @property
    def owner(self):
        return self.agente.user


class PublicacionVivienda(Publicacion):
    TIPOS_NEGOCIO = (
        ('arriendo', 'Arriendo'),
        ('venta', 'Venta'),
    )

    tipo_negocio = models.CharField(max_length=32, choices=TIPOS_NEGOCIO)
    propiedad = models.ForeignKey(Vivienda, related_name='publicaciones', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'PublicacionVivienda'
        verbose_name_plural = 'Publicaciones Viviendas'


class PublicacionComercial(Publicacion):
    TIPOS_NEGOCIO = (
        ('arriendo', 'Arriendo'),
        ('venta', 'Venta'),
    )

    tipo_negocio = models.CharField(max_length=32, choices=TIPOS_NEGOCIO)
    propiedad = models.ForeignKey(Comercial, related_name='publicaciones', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'PublicacionComercial'
        verbose_name_plural = 'Publicaciones Comerciales'


class PublicacionIndustrial(Publicacion):
    TIPOS_NEGOCIO = (
        ('arriendo', 'Arriendo'),
        ('venta', 'Venta'),
    )

    tipo_negocio = models.CharField(max_length=32, choices=TIPOS_NEGOCIO)
    propiedad = models.ForeignKey(Industrial, related_name='publicaciones', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'PublicacionIndustrial'
        verbose_name_plural = 'Publicaciones Industriales'


class PublicacionLotes(Publicacion):
    TIPOS_NEGOCIO = (
        ('arriendo', 'Arriendo'),
        ('venta', 'Venta'),
    )

    tipo_negocio = models.CharField(max_length=32, choices=TIPOS_NEGOCIO)
    propiedad = models.ForeignKey(Lotes, related_name='publicaciones', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'PublicacionLotes'
        verbose_name_plural = 'Publicaciones Lotes'
