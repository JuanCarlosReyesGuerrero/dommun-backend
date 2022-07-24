from django.contrib.auth.models import User
from django.db import models

from agentes.models import Agente
from zonas.models import Zona


class Cliente(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        unique=True,
        related_name='cliente', on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=120, null=True, blank=True)
    apellido = models.CharField(max_length=120, null=True, blank=True)
    nacionalidad = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(null=True, blank=False)
    telefono_principal = models.CharField(max_length=32, null=True, blank=False)
    telefono_secundario = models.CharField(max_length=32, null=True, blank=True)
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    agente = models.ForeignKey(
        Agente,
        null=True,
        blank=True,
        related_name='clientes', on_delete=models.CASCADE
    )

    @property
    def owner(self):
        return self.agente.user

    @property
    def get_current_necesidad(self):
        try:
            return Necesidad.objects.filter(activo=True, cliente=self).first()
        except:
            return None

    def get_nombre_completo(self):
        return "%s %s" % (self.nombre, self.apellido)

    def primary_phone(self):
        for type in ('office', 'mobile', 'home'):
            for location in self.user.locations.all():
                for phone in location.phones.all():
                    if phone.type == type:
                        return phone

        return None

    def __str__(self):
        return "%s %s" % (self.nombre, self.apellido)

    class Meta:
        ordering = ('nombre', 'apellido')


class Necesidad(models.Model):
    from propiedades.models import Propiedad
    cliente = models.ForeignKey(
        Cliente,
        null=False,
        blank=False,
        unique=False,
        related_name='necesidades', on_delete=models.CASCADE
    )

    TIPOS_URGENCIA = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    tipo_urgencia = models.CharField(max_length=32, choices=TIPOS_URGENCIA, default='C')

    TIPOS_NEGOCIO = (
        ('arriendo', 'Arriendo'),
        ('compra', 'Compra'),
        ('venta', 'Venta'),
    )

    tipo_negocio = models.CharField(max_length=32, choices=TIPOS_NEGOCIO)
    notas = models.TextField(null=True, blank=True)
    precio_min = models.DecimalField(max_digits=17, decimal_places=2, null=False, blank=False)
    precio_max = models.DecimalField(max_digits=17, decimal_places=2, null=False, blank=False)
    area_min = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    area_max = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    habitaciones_min = models.IntegerField(null=False, blank=False)
    parqueaderos_min = models.IntegerField(null=False, blank=False)
    banos_min = models.IntegerField(null=False, blank=False)
    zonas = models.ManyToManyField(Zona, related_name='necesidades')

    propiedad_primer_contacto = models.ForeignKey(
        Propiedad,
        null=True,
        blank=True, on_delete=models.CASCADE
    )

    antiguedad_max = models.IntegerField(null=False, default=5)
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)
    activo = models.BooleanField(null=False, default=True)

    @property
    def owner(self):
        return self.cliente.agente.user

    class Meta:
        verbose_name = 'Necesidad'
        verbose_name_plural = 'Necesidades'

    def save(self, *args, **kwargs):
        if self._state.adding and self.activo:
            necesidades = Necesidad.objects.filter(cliente=self.cliente, activo=True)
            for necesidad in necesidades:
                necesidad.activo = False
                necesidad.save()
        super(Necesidad, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s" % (self.cliente.nombre, self.cliente.apellido)


class PropiedadNecesidad(models.Model):
    from publicaciones.models import PublicacionVivienda
    necesidad = models.ForeignKey(
        Necesidad,
        null=False,
        blank=False,
        related_name='propiedades',
        limit_choices_to={'activo': True}, on_delete=models.CASCADE

    )
    publicacion = models.ForeignKey(
        PublicacionVivienda,
        null=False,
        blank=False, on_delete=models.CASCADE
    )

    # cita
    cita = models.DateTimeField(null=True, blank=True)
    notas_cita = models.TextField(null=True, blank=True)
    valor_propiedad_inicial = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    valor_oferta = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    valor_hipoteca = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    valor_arras = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    aseguradora = models.CharField(max_length=100, null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    fecha_firma_promesa = models.DateTimeField(null=True, blank=True)

    # estados funnel
    ESTADOS = (
        (0, 'Agregado Manualmente'),
        (1, 'Enviado'),
        (2, 'Visita'),
        (3, 'Oferta'),
        (4, 'Cierre'),
    )

    estado = models.IntegerField('Estado', null=False, blank=False, default=1, choices=ESTADOS)
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    @property
    def owner(self):
        return self.necesidad.cliente.agente.user

    class Meta:
        verbose_name = 'Propiedad vs Necesidad'
        verbose_name_plural = 'Propiedades vs Necesidades'
        unique_together = ("necesidad", "publicacion")
