import random

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models

from zonas.models import Zona, Municipio


def upload_foto_agente(instance, filename):
    import os
    filename_base, filename_ext = os.path.splitext(filename)
    from django.utils.timezone import now
    return 'agenphotos/' + str(instance.id) + '/%s%s' % (
        now().strftime("%Y%m%d%H%M%S") + "" + str(random.randint(1, 1000000)),
        filename_ext.lower(),
    )


# Descripción del perfil del agente en pdf
def upload_docs_agente(instance, filename):
    import os
    import random
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    return 'agenphotos/' + str(instance.id) + '/%s%s' % (
        now().strftime("%Y%m%d%H%M%S") + "" + str(random.randint(1, 1000000)),
        filename_ext.lower(),
    )


# Create your models here.
# ************************************************************
# Esta clase maneja los planes de membresía
# ************************************************************
class PlanMembresia(models.Model):
    nombre = models.CharField(null=True, blank=True, max_length=255)
    precio_promocion = models.DecimalField(max_digits=17, decimal_places=2, null=False, blank=False)
    precio_fijo = models.DecimalField(max_digits=17, decimal_places=2, null=False, blank=False)
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Planes Membresía"
        verbose_name = "Plan Membresía"


class Agente(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        unique=True,
        related_name='agente', on_delete=models.CASCADE
    )
    slug = models.SlugField(null=False, blank=True)
    nombre = models.CharField(max_length=120, null=True, blank=True)
    apellido = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefono_contacto = models.CharField(null=True, blank=True, max_length=80)
    descripcion = models.TextField(null=True, blank=True)

    zonas_appto = models.ManyToManyField(Zona, blank=True, limit_choices_to={'tipo_zona': 'appto'},
                                         related_name='zonas_appto')
    ciudades = models.ManyToManyField(Zona, blank=True, limit_choices_to={'tipo_zona': 'ciudad'})
    foto_perfil = models.ImageField(upload_to=upload_foto_agente, blank=True, null=True)

    acepta_arriendo = models.BooleanField(null=False, default=True)
    acepta_venta = models.BooleanField(null=False, default=True)

    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    activo = models.BooleanField(null=False, default=True, blank=False)
    publicado = models.BooleanField(null=False, default=True, blank=False)

    precio_arriendo_min = models.BigIntegerField(null=True, blank=True, default=1500000)
    precio_venta_min = models.BigIntegerField(null=True, blank=True, default=250000000)

    ZONIFICACION = (
        ('bogota', 'Bogotá'),
        ('barranquilla', 'Barranquilla'),
        ('medellin', 'Medellín'),
    )

    zonificacion = models.CharField(max_length=32, choices=ZONIFICACION)
    redes_sociales = JSONField(default={'facebook': 'null', 'instagram': 'null'})
    descripcion_perfil = models.FileField(upload_to=upload_docs_agente, blank=True, null=True)
    numero_avaluo = models.IntegerField(null=False, default=0)
    municipio = models.ForeignKey(Municipio, null=True, blank=True, verbose_name='Ciudad', related_name='agentes', on_delete=models.CASCADE)
    fecha_inicio_plan = models.DateTimeField(null=True, blank=True)
    plan_membresia = models.ForeignKey(PlanMembresia, null=True, blank=True, verbose_name='Plan', related_name='agentes', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + " " + self.apellido

    def get_ciudades(self):
        return "\n".join([c.nombre for c in self.ciudades.all()])

    def get_zonas_appto(self):
        return "\n".join([c.nombre for c in self.zonas_appto.all()])

    def save(self, *args, **kwargs):
        from django.contrib.auth.models import Group

        if self.activo:
            if self.user is None:
                user = User.objects.create_user(username=self.slug,
                                                email=self.email,
                                                first_name=self.nombre,
                                                last_name=self.apellido, password='FAJSflk-ehqKLY570TY34P87')
                g = Group.objects.get(name='agentes')
                g.user_set.add(user)
                self.user = user
        super(Agente, self).save(*args, **kwargs)

    class Meta:
        ordering = ('nombre', 'apellido')


# ************************************************************
# Maneja la ubicación del archivo
# ************************************************************
def upload_docs_gestion_documental(instance, filename):
    import os
    import random
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    return 'documentos/' + 'gestiondocumental/' + '/%s%s' % (
        now().strftime("%Y%m%d%H%M%S") + "" + str(random.randint(1, 1000000)),
        filename_ext.lower(),
    )


# ************************************************************
# Esta clase maneja la gestión documental
# ************************************************************
class GestionDocumental(models.Model):
    nombre = models.CharField(null=True, blank=True, max_length=255)
    documento_subido = models.FileField(upload_to=upload_docs_gestion_documental, blank=True, null=True)

    DOCU_PRECONFIGURADO = 1
    AGENTE_IDEAL = 2

    CATEGORIAS = (
        (DOCU_PRECONFIGURADO, 'Documentos preconfigurados'),
        (AGENTE_IDEAL, '¿Cómo ser un agente ideal?'),
    )

    categoria = models.IntegerField(null=False, choices=CATEGORIAS, default=DOCU_PRECONFIGURADO)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Gestión documental"
        verbose_name = "Gestión documental"
