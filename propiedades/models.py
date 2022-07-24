from django.db import models

from agentes.models import Agente
from clientes.models import Cliente
from zonas.models import Municipio

from django.conf import settings

from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver
from django.utils.timezone import now
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from versatileimagefield.fields import VersatileImageField

try:
    from polymorphic.models import PolymorphicModel
    from polymorphic.managers import PolymorphicManager
except ImportError:
    # django-polymorphic < 0.8
    from polymorphic import PolymorphicModel, PolymorphicManager


def upload_foto_propiedad(instance, filename):
    import os
    import random
    filename_base, filename_ext = os.path.splitext(filename)
    return 'fotografias/' + str(instance.propiedad.id) + '/opt/%s%s' % (
        now().strftime("%Y%m%d%H%M%S") + "" + str(random.randint(1, 1000000)),
        filename_ext.lower(),
    )


def upload_documentos_personas(instance, filename):
    import os
    import random

    filename_base, filename_ext = os.path.splitext(filename)
    return 'documentos/%s%s' % (
        now().strftime("%Y%m%d") + "" + str(random.randint(1, 100)) + "-" + filename_base.lower(),
        filename_ext.lower(),
    )


class Fotografia(models.Model):
    image = VersatileImageField('Image', upload_to=upload_foto_propiedad, blank=False, null=False)
    propiedad = models.ForeignKey('Propiedad', null=False, related_name='fotografias', on_delete=models.CASCADE)
    valida = models.BooleanField(null=False, default=False)
    es_fotografia_principal = models.BooleanField(null=False, default=False)
    orden = models.IntegerField(null=False, default=0)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Fotografía'
        verbose_name_plural = 'Fotografías'

    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

    def __str__(self):
        return str(self.id) + " i:" + str(self.propiedad)


@receiver(models.signals.post_save, sender=Fotografia)
def warm_fotografia_headshot_images(sender, instance, **kwargs):
    """Ensures Person head shots are created post-save"""
    fotografia_img_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='fotografias',
        image_attr='image'
    )
    num_created, failed_to_create = fotografia_img_warmer.warm()


class TipoDocumentoPropiedad(models.Model):
    nombre_documento = models.CharField('Nombre del Documento', max_length=120)
    requisito_publicacion = models.BooleanField('Requisito para publicación', default=False)
    descripcion = models.TextField('Descripcion', blank=True)

    class Meta:
        verbose_name = 'Tipo de Documento de la  Propiedad'
        verbose_name_plural = 'Tipos de Documento de la Propiedad'

    def __str__(self):
        return str(self.nombre_documento)


class DocumentoPropiedad(models.Model):
    tipo_documento = models.ForeignKey(TipoDocumentoPropiedad, null=False, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to=upload_documentos_personas, blank=False, null=False)
    propiedad = models.ForeignKey('Propiedad', null=False, related_name='archivos', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Documento de la Propiedad'
        verbose_name_plural = 'Documentos de las Propiedades'

    def __str__(self):
        return str(self.tipo_documento)


class Caracteristica(models.Model):
    nombre = models.CharField(db_index=True, unique=True, null=False, blank=False, max_length=80)

    TIPOS_CARACTERISTICA = (
        (1, 'Interior'),
        (2, 'Exterior'),
        (3, 'De la zona'),
    )
    aplica_apartamento = models.BooleanField(null=False, default=False)
    aplica_casa = models.BooleanField(null=False, default=False)
    aplica_oficina = models.BooleanField(null=False, default=False)
    aplica_bodega = models.BooleanField(null=False, default=False)
    aplica_local = models.BooleanField(null=False, default=False)
    aplica_lote = models.BooleanField(null=False, default=False)
    tipo_caracteristica = models.IntegerField(null=False, choices=TIPOS_CARACTERISTICA, default=1)

    def __str__(self):
        return str(self.nombre)


class Propiedad(PolymorphicModel):
    matricula_inmobiliaria = models.CharField(null=True, blank=True, max_length=100)
    agente = models.ForeignKey(Agente, null=False, blank=False, related_name='propiedades',
                               limit_choices_to={'activo': True}, on_delete=models.CASCADE)
    propietario = models.ForeignKey(Cliente, null=False, blank=False, related_name='propiedades',
                                    on_delete=models.CASCADE)
    direccion = JSONField(default={'estado': 'null'})
    caracteristicas = JSONField(default={})
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)
    descripcion = models.TextField(null=True, blank=True)
    linkvirtual360 = models.CharField(null=True, blank=True, max_length=100, verbose_name='Link virtual 360')
    avaluo = JSONField(default={'estado': 'null'})
    coordenadas = models.CharField(null=True, blank=True, max_length=100, verbose_name='coordenadas long lat',
                                   default='0 0')
    municipio = models.ForeignKey(Municipio, null=True, blank=True, verbose_name='Ciudad', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def get_publicacion(self):
        from publicaciones.models import PublicacionVivienda

        try:
            publicacion = PublicacionVivienda.objects.filter(estado=PublicacionVivienda.ESTADO_PUBLICADO,
                                                             propiedad=self).first()
            return publicacion
        except Exception as e:
            return None

    def get_publicacion_comercial(self):
        from publicaciones.models import PublicacionComercial

        try:
            publicacion = PublicacionComercial.objects.filter(estado=PublicacionComercial.ESTADO_PUBLICADO,
                                                              propiedad=self).first()
            return publicacion
        except Exception as e:
            return None

    def get_publicacion_industrial(self):
        from publicaciones.models import PublicacionIndustrial

        try:
            publicacion = PublicacionIndustrial.objects.filter(estado=PublicacionIndustrial.ESTADO_PUBLICADO,
                                                               propiedad=self).first()
            return publicacion
        except Exception as e:
            return None

    def get_publicacion_lotes(self):
        from publicaciones.models import PublicacionLotes

        try:
            publicacion = PublicacionLotes.objects.filter(estado=PublicacionLotes.ESTADO_PUBLICADO,
                                                          propiedad=self).first()
            return publicacion
        except Exception as e:
            return None

    def get_caracteristicas(self):
        caracteristicas = Caracteristica.objects.filter(id__in=self.caracteristicas)

        return caracteristicas

    def get_fotografiaPrincipal(self):

        try:
            foto = Fotografia.objects.filter(propiedad=self, es_fotografia_principal=True).first()
            return foto
        except:
            return ""

    @property
    def owner(self):
        return self.agente.user

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        ordering = ('-id', 'polymorphic_ctype_id')


class Vivienda(Propiedad):
    TIPOS_VIVIENDA = (
        (1, 'Apartamento'),
        (2, 'Casa'),
    )
    tipo_vivienda = models.IntegerField(null=False, choices=TIPOS_VIVIENDA,
                                        default=1)

    habitaciones = models.IntegerField(null=True, blank=True, verbose_name='Número de habitaciones',
                                       help_text='No Incluyen cuartos de servicio', default=0)
    estudios = models.IntegerField(null=True, blank=True, verbose_name='Número de estudios',
                                   help_text='', default=0)
    habitaciones_auxiliares = models.IntegerField(null=True, blank=True,
                                                  verbose_name='Número de cuartos de servicio',
                                                  help_text='', default=0)
    banos = models.IntegerField(null=True, blank=True, verbose_name='Número de baños',
                                help_text='', default=0)
    banos_sociales = models.IntegerField(null=True, blank=True, verbose_name='Número de baños sociales',
                                         help_text='', default=0)
    banos_servicio = models.IntegerField(null=True, blank=True, verbose_name='Número de baños de servicio',
                                         help_text='', default=0)

    anio_construccion = models.IntegerField(null=True, blank=True, verbose_name='Año de construcción',
                                            help_text='', default=0)

    balcones = models.IntegerField(null=True, blank=True, verbose_name='Número de balcones', default=0)
    terrazas = models.IntegerField(null=True, blank=True, verbose_name='Número de terrazas', default=0)

    area_privada = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8,
                                       verbose_name='Área privada')
    area_construida = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8,
                                          verbose_name='Área construida')
    area_terraza = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5,
                                       verbose_name='Área terraza')
    area_lote = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8, verbose_name='Área lote')

    TIPO_ESTACIONAMIENTO_N_A = 0
    TIPO_ESTACIONAMIENTO_EN_FILA = 1
    TIPO_ESTACIONAMIENTO_INDEPENDIENTES = 2

    TIPOS_ESTACIONAMIENTO = (
        (TIPO_ESTACIONAMIENTO_N_A, 'N/A'),
        (TIPO_ESTACIONAMIENTO_EN_FILA, 'En fila'),
        (TIPO_ESTACIONAMIENTO_INDEPENDIENTES, 'Independientes'),
    )

    tipo_estacionamientos = models.IntegerField(null=False, choices=TIPOS_ESTACIONAMIENTO,
                                                default=TIPO_ESTACIONAMIENTO_EN_FILA)
    estacionamientos_cubiertos = models.IntegerField(null=True, blank=True, verbose_name='Número de garajes cubiertos',
                                                     default=0)
    estacionamientos_descubiertos = models.IntegerField(null=True, blank=True,
                                                        verbose_name='Número de garajes descubiertos',
                                                        default=0)
    estacionamientos_totales = models.IntegerField(null=True, blank=True,
                                                   verbose_name='Número total de garajes',
                                                   help_text='Cubiertos y descubiertos', default=0)
    amoblado = models.BooleanField(null=False, default=False)
    estrato = models.IntegerField(null=True, blank=True)
    deposito = models.BooleanField(null=False, default=False)

    @property
    def antiguedad(self):
        import datetime
        return datetime.datetime.today().year - self.anio_construccion


class Comercial(Propiedad):
    TIPOS = (
        (1, 'Local'),
        (2, 'Oficinas'),
    )
    tipo = models.IntegerField(null=False, choices=TIPOS,
                               default=1)
    espacios = models.IntegerField(null=True, blank=True, verbose_name='Número de espacios',
                                   help_text='', default=0)
    cocineta = models.BooleanField(null=False, default=False)
    banos = models.IntegerField(null=True, blank=True, verbose_name='Número de baños',
                                help_text='', default=0)
    anio_construccion = models.IntegerField(null=True, blank=True, verbose_name='Año de construcción',
                                            help_text='', default=0)
    balcones = models.IntegerField(null=True, blank=True, verbose_name='Número de balcones', default=0)
    terrazas = models.IntegerField(null=True, blank=True, verbose_name='Número de terrazas', default=0)
    area_privada = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8,
                                       verbose_name='Área privada')
    area_construida = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8,
                                          verbose_name='Área construida')
    area_terraza = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5,
                                       verbose_name='Área terraza')

    TIPO_ESTACIONAMIENTO_N_A = 0
    TIPO_ESTACIONAMIENTO_EN_FILA = 1
    TIPO_ESTACIONAMIENTO_INDEPENDIENTES = 2

    TIPOS_ESTACIONAMIENTO = (
        (TIPO_ESTACIONAMIENTO_N_A, 'N/A'),
        (TIPO_ESTACIONAMIENTO_EN_FILA, 'En fila'),
        (TIPO_ESTACIONAMIENTO_INDEPENDIENTES, 'Independientes'),
    )

    tipo_estacionamientos = models.IntegerField(null=False, choices=TIPOS_ESTACIONAMIENTO,
                                                default=TIPO_ESTACIONAMIENTO_EN_FILA)
    estacionamientos_cubiertos = models.IntegerField(null=True, blank=True, verbose_name='Número de garajes cubiertos',
                                                     default=0)
    estacionamientos_descubiertos = models.IntegerField(null=True, blank=True,
                                                        verbose_name='Número de garajes descubiertos', default=0)
    estacionamientos_totales = models.IntegerField(null=True, blank=True,
                                                   verbose_name='Número total de garajes',
                                                   help_text='Cubiertos y descubiertos', default=0)

    amoblado = models.BooleanField(null=False, default=False)
    estrato = models.IntegerField(null=True, blank=True)
    deposito = models.BooleanField(null=False, default=False)

    @property
    def antiguedad(self):
        import datetime
        return datetime.datetime.today().year - self.anio_construccion

    class Meta:
        verbose_name = 'Comercial'
        verbose_name_plural = 'Comerciales'


class Industrial(Propiedad):
    TIPOS = (
        (1, 'Bodega'),
    )
    tipo = models.IntegerField(null=False, choices=TIPOS,
                               default=1)
    espacios = models.IntegerField(null=True, blank=True, verbose_name='Número de espacios',
                                   help_text='', default=0)
    banos = models.IntegerField(null=True, blank=True, verbose_name='Número de baños',
                                help_text='', default=0)
    anio_construccion = models.IntegerField(null=True, blank=True, verbose_name='Año de construcción',
                                            help_text='', default=0)
    area_privada = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8,
                                       verbose_name='Área privada')
    area_construida = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8,
                                          verbose_name='Área construida')
    area_lote = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8, verbose_name='Área lote')

    @property
    def antiguedad(self):
        import datetime
        return datetime.datetime.today().year - self.anio_construccion

    class Meta:
        verbose_name = 'Industrial'
        verbose_name_plural = 'Industriales'


class Lotes(Propiedad):
    TIPOS = (
        (1, 'Lote Industrial'),
        (2, 'Lote Vivienda'),
    )
    tipo = models.IntegerField(null=False, choices=TIPOS,
                               default=1)
    area_lote = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8, verbose_name='Área lote')

    @property
    def antiguedad(self):
        import datetime
        return datetime.datetime.today().year - self.anio_construccion

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
