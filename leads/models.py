import decimal
from ckeditor.fields import RichTextField
from django.db import models

from propiedades.models import Propiedad
from agentes.models import Agente
from clientes.models import Cliente, Necesidad, PropiedadNecesidad
from publicaciones.models import PublicacionVivienda, PublicacionComercial, PublicacionIndustrial, PublicacionLotes

from django.core.mail import send_mail
from django.db import transaction
from django.utils import formats

from zonas.models import Municipio


class Consignacion(models.Model):
    agente = models.ForeignKey(Agente, null=False, blank=False, limit_choices_to={'activo': True}, on_delete=models.CASCADE)

    ESTADOS_CREADO_POR_WEB = 0
    ESTADOS_TRAMITADO = 1
    ESTADOS_ASIGNADO_AGENTE = 3
    ESTADOS_NO_INTERESA = 4
    ESTADOS_NO_ACEPTA_COND = 5

    ESTADOS = (
        (ESTADOS_CREADO_POR_WEB, 'Creado por web'),
        (ESTADOS_TRAMITADO, 'Tramitado por Operaciones'),
        (ESTADOS_ASIGNADO_AGENTE, 'Asignado a agente'),
        (ESTADOS_NO_INTERESA, 'No interesa'),
        (ESTADOS_NO_ACEPTA_COND, 'Cliente no acepta cond.')
    )
    estado = models.IntegerField(null=False, choices=ESTADOS, default=ESTADOS_CREADO_POR_WEB)

    TIPO_CONSIGNACION_NO_DETERMINADA = 0
    TIPO_CONSIGNACION_ARRIENDO = 1
    TIPO_CONSIGNACION_VENTA = 2
    TIPO_CONSIGNACION_OTRO = 3
    TIPO_CONSIGNACION = (
        (TIPO_CONSIGNACION_NO_DETERMINADA, 'No determina'),
        (TIPO_CONSIGNACION_ARRIENDO, 'Arriendo'),
        (TIPO_CONSIGNACION_VENTA, 'Venta'),
        (TIPO_CONSIGNACION_OTRO, 'Otro'),
    )
    tipo_consignacion = models.IntegerField(null=False, choices=TIPO_CONSIGNACION,
                                            default=TIPO_CONSIGNACION_NO_DETERMINADA)

    nombre = models.CharField(null=True, blank=True, max_length=120)
    apellido = models.CharField(null=True, blank=True, max_length=120)
    telefono = models.CharField(null=True, blank=True, max_length=30)
    email = models.EmailField(null=False, blank=False)

    comentarios = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    # ******************************************
    PRECIO_ESTIMADO_CERO_MILLON = 0
    PRECIO_ESTIMADO_MILLON_DIEZMILLONES = 1
    PRECIO_ESTIMADO_DIEZMILLONES_CINCUENTAMILLONES = 2
    PRECIO_ESTIMADO_CINCUENTAMILLONES_CIENMILLONES = 3
    PRECIO_ESTIMADO = (
        (PRECIO_ESTIMADO_CERO_MILLON, '0 a $1.000.000'),
        (PRECIO_ESTIMADO_MILLON_DIEZMILLONES, '$1.000.000 a $10.000.000'),
        (PRECIO_ESTIMADO_DIEZMILLONES_CINCUENTAMILLONES, '$10.000.000 a $50.000.000'),
        (PRECIO_ESTIMADO_CINCUENTAMILLONES_CIENMILLONES, '$50.000.000 a $100.000.000'),
    )
    precio_estimado = models.IntegerField(null=False, choices=PRECIO_ESTIMADO,
                                          default=PRECIO_ESTIMADO_CERO_MILLON)

    TIPO_INMUEBLE_VIVIENDA = 0
    TIPO_INMUEBLE_APARTAMENTO = 1
    TIPO_INMUEBLE_OFICINA = 2
    TIPO_INMUEBLE_LOCAL = 3
    TIPO_INMUEBLE_BODEGA = 4
    TIPO_INMUEBLE_LOTE = 5
    TIPO_INMUEBLE = (
        (TIPO_INMUEBLE_VIVIENDA, 'Casa'),
        (TIPO_INMUEBLE_APARTAMENTO, 'Apartamento'),
        (TIPO_INMUEBLE_OFICINA, 'Oficina'),
        (TIPO_INMUEBLE_LOCAL, 'Local'),
        (TIPO_INMUEBLE_BODEGA, 'Bodega'),
        (TIPO_INMUEBLE_LOTE, 'Lote'),
    )
    tipo_inmueble = models.IntegerField(null=False, choices=TIPO_INMUEBLE,
                                        default=TIPO_INMUEBLE_VIVIENDA)

    municipio = models.ForeignKey(Municipio, null=True, blank=True, verbose_name='Ciudad',
                                  related_name='consignaciones', on_delete=models.CASCADE)

    zona = models.CharField(null=True, blank=True, max_length=120)
    metraje = models.DecimalField(max_digits=17, decimal_places=2, null=False, blank=False, default=0)
    habitaciones = models.IntegerField(null=True, blank=True, default=0)
    banos = models.IntegerField(null=True, blank=True, default=0)
    garajes = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.fecha_creacion) + ' ' + str(self.nombre) + ' - ' + str(self.apellido)

    def save(self, *args, **kwargs):
        from slacker import Slacker

        if self.estado == Consignacion.ESTADOS_CREADO_POR_WEB:
            try:
                slack = Slacker('xoxb-43612317654-UnhAHi6ajw0bmmfxmHHee6J6')
                slack.chat.post_message(channel='#consignaciones',
                                        text='Tenemos una nueva consignación de ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + '',
                                        username="crm")
            except:
                pass

        super(Consignacion, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Consignación'
        verbose_name_plural = 'Consignaciones'


class Administracion(models.Model):
    ESTADOS_CREADO_POR_WEB = 0
    ESTADOS_TRAMITADO = 1
    ESTADOS_FINALIZADO = 3
    ESTADOS_NO_INTERESA = 4

    ESTADOS = (
        (ESTADOS_CREADO_POR_WEB, 'Creado por web'),
        (ESTADOS_TRAMITADO, 'Tramitado por Operaciones'),
        (ESTADOS_FINALIZADO, 'Finalizado'),
        (ESTADOS_NO_INTERESA, 'No interesa'),
    )
    estado = models.IntegerField(null=False, choices=ESTADOS, default=ESTADOS_CREADO_POR_WEB)

    nombre = models.CharField(null=True, blank=True, max_length=120)
    apellido = models.CharField(null=True, blank=True, max_length=120)
    telefono = models.CharField(null=True, blank=True, max_length=30)
    email = models.EmailField(null=False, blank=False)

    comentarios = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return str(self.fecha_creacion) + ' ' + str(self.nombre) + ' - ' + str(self.apellido)

    def save(self, *args, **kwargs):
        from slacker import Slacker

        if self.estado == Administracion.ESTADOS_CREADO_POR_WEB:
            try:
                slack = Slacker('xoxb-43612317654-UnhAHi6ajw0bmmfxmHHee6J6')
                slack.chat.post_message(channel='#imnadmon',
                                        text='Tenemos una nueva consignación en administración de ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + '',
                                        username="crm")
            except:
                pass

        super(Administracion, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Administración'
        verbose_name_plural = 'Administraciones'


class PromotorCandidato(models.Model):
    ESTADOS_CREADO_POR_WEB = 0
    ESTADOS_TRAMITADO = 1
    ESTADOS_FINALIZADO = 3
    ESTADOS_NO_INTERESA = 4

    ESTADOS = (
        (ESTADOS_CREADO_POR_WEB, 'Creado por web'),
        (ESTADOS_TRAMITADO, 'Tramitado por Operaciones'),
        (ESTADOS_FINALIZADO, 'Finalizado'),
        (ESTADOS_NO_INTERESA, 'No interesa'),
    )
    estado = models.IntegerField(null=False, choices=ESTADOS, default=ESTADOS_CREADO_POR_WEB)

    nombre = models.CharField(null=True, blank=True, max_length=120)
    apellido = models.CharField(null=True, blank=True, max_length=120)
    telefono = models.CharField(null=True, blank=True, max_length=30)
    email = models.EmailField(null=False, blank=False)

    CIUDADES_BOGOTA = 0
    CIUDADES_BARRANQUILLA = 1
    CIUDADES_OTRA = 2

    CIUDADES = (
        (CIUDADES_BOGOTA, 'Bogotá'),
        (CIUDADES_BARRANQUILLA, 'Barranquilla'),
        (CIUDADES_OTRA, 'Otra'),
    )
    ciudad = models.IntegerField(null=False, choices=CIUDADES, default=CIUDADES_BOGOTA)

    MODO_TRABAJO_INDEPENDIENTE = 0
    MODO_TRABAJO_INMOBILIARIA = 1
    MODO_TRABAJO_OTRO = 2

    MODO_TRABAJO = (
        (MODO_TRABAJO_INDEPENDIENTE, 'Independiente'),
        (MODO_TRABAJO_INMOBILIARIA, 'Trabajo con Inmobiliaria'),
        (MODO_TRABAJO_OTRO, 'Otro'),
    )
    modo_trabajo = models.IntegerField(null=False, choices=MODO_TRABAJO, default=MODO_TRABAJO_INDEPENDIENTE)

    comentarios = models.TextField(null=True, blank=True)

    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    municipio = models.ForeignKey(Municipio, null=True, blank=True, verbose_name='Ciudad', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha_creacion) + ' ' + str(self.nombre) + ' - ' + str(self.apellido)

    def save(self, *args, **kwargs):
        from slacker import Slacker

        if self.estado == PromotorCandidato.ESTADOS_CREADO_POR_WEB:
            try:
                slack = Slacker('xoxb-43612317654-UnhAHi6ajw0bmmfxmHHee6J6')
                slack.chat.post_message(channel='#candidatos',
                                        text='Tenemos un nuevo candidato: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + '',
                                        username="crm")
            except:
                pass

        super(PromotorCandidato, self).save(*args, **kwargs)


class ContactoPortales(models.Model):
    TIPOS_NEGOCIO = (
        ('arriendo', 'Arriendo'),
        ('compra', 'Compra'),
        ('no_interesa', 'No interesa'),
    )

    tipo_negocio = models.CharField(max_length=32, choices=TIPOS_NEGOCIO)
    propiedad = models.ForeignKey(Propiedad, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(null=True, blank=True, max_length=120)
    apellido = models.CharField(null=True, blank=True, max_length=120)
    telefono = models.CharField(null=True, blank=True, max_length=30)
    email = models.EmailField(null=True, blank=True)
    content = RichTextField()
    medio_de_contacto = models.TextField(null=True, blank=True)
    mensaje_usuario = models.TextField(null=True, blank=True)
    ha_creado_sol_contacto = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    ESTADOS_CREADO_POR_WEB = 0
    ESTADOS_TRAMITADO = 1
    ESTADOS_CORREO_NO_APLICA = 3
    ESTADOS_NO_INTERESA = 4

    ESTADOS = (
        (ESTADOS_CREADO_POR_WEB, 'Creado por web'),
        (ESTADOS_TRAMITADO, 'Requerimiento CREADO'),
        (ESTADOS_CORREO_NO_APLICA, 'Correo no aplica para requerimiento'),
        (ESTADOS_NO_INTERESA, 'No interesa'),
    )
    estado = models.IntegerField(null=False, choices=ESTADOS, default=ESTADOS_CREADO_POR_WEB)

    def __str__(self):
        return str(self.estado) + ' ' + str(self.fecha_creacion) + ' ' + str(self.nombre) + ' - ' + str(self.apellido)

    def save(self, *args, **kwargs):
        from slacker import Slacker

        if self.estado == ContactoPortales.ESTADOS_CREADO_POR_WEB:
            try:
                slack = Slacker('xoxb-43612317654-UnhAHi6ajw0bmmfxmHHee6J6')
                slack.chat.post_message(channel='#contactoportales',
                                        text='Tenemos un nuevo contacto de portales que necesita ser procesado',
                                        username="crm")
            except:
                pass

        if self.estado == ContactoPortales.ESTADOS_TRAMITADO and self.ha_creado_sol_contacto:

            # Publicación Vivienda
            try:
                with transaction.atomic():
                    publicacion2 = PublicacionVivienda.objects.get(propiedad=self.propiedad,
                                                                   estado=PublicacionVivienda.ESTADO_PUBLICADO)
                    send_mail(
                        'Tienes un nuevo contacto portales',
                        'Tienes un nuevo contacto que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + str(
                            self.propiedad_id),
                        'portales@appto.co',
                        [publicacion2.agente.email],
                        fail_silently=False,
                    )

                    publicacion = PublicacionVivienda.objects.get(propiedad=self.propiedad,
                                                                  estado=PublicacionVivienda.ESTADO_PUBLICADO,
                                                                  tipo_negocio=self.tipo_negocio)
                    cliente = None
                    try:
                        cliente = Cliente.objects.get(email=self.email)

                        necesidad = None
                        try:
                            necesidad = Necesidad.objects.get(cliente=cliente, activo=True)
                        except Necesidad.DoesNotExist:
                            necesidad = Necesidad.objects.create(cliente=cliente,
                                                                 precio_min=publicacion.precio * decimal.Decimal(0.8),
                                                                 precio_max=publicacion.precio * decimal.Decimal(1.2),
                                                                 area_min=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                     0.8),
                                                                 area_max=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                     1.2),
                                                                 tipo_negocio=publicacion.tipo_negocio,
                                                                 notas=self.mensaje_usuario,
                                                                 habitaciones_min=publicacion.propiedad.habitaciones,
                                                                 parqueaderos_min=publicacion.propiedad.estacionamientos_totales,
                                                                 banos_min=publicacion.propiedad.banos,
                                                                 propiedad_primer_contacto=self.propiedad,
                                                                 activo=True)

                        PropiedadNecesidad.objects.create(necesidad=necesidad,
                                                          publicacion=publicacion,
                                                          valor_propiedad_inicial=publicacion.precio, )


                    except Cliente.DoesNotExist:
                        cliente = Cliente.objects.create(nombre=self.nombre, apellido=self.apellido,
                                                         nacionalidad='Colombia',
                                                         email=self.email, telefono_principal=self.telefono)

                        necesidad = Necesidad.objects.create(cliente=cliente,
                                                             precio_min=publicacion.precio * decimal.Decimal(0.8),
                                                             precio_max=publicacion.precio * decimal.Decimal(1.2),
                                                             area_min=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                 0.8),
                                                             area_max=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                 1.2),
                                                             tipo_negocio=publicacion.tipo_negocio,
                                                             notas=self.mensaje_usuario,
                                                             habitaciones_min=publicacion.propiedad.habitaciones,
                                                             parqueaderos_min=publicacion.propiedad.estacionamientos_totales,
                                                             banos_min=publicacion.propiedad.banos,
                                                             propiedad_primer_contacto=self.propiedad,
                                                             activo=True)

                        PropiedadNecesidad.objects.create(necesidad=necesidad,
                                                          publicacion=publicacion,
                                                          valor_propiedad_inicial=publicacion.precio, )

            # except PublicacionVivienda.DoesNotExist:
            except:
                pass

            # Publicación Comercial
            try:
                with transaction.atomic():
                    publicacion2 = PublicacionComercial.objects.get(propiedad=self.propiedad,
                                                                    estado=PublicacionComercial.ESTADO_PUBLICADO)
                    send_mail(
                        'Tienes un nuevo contacto portales',
                        'Tienes un nuevo contacto que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + str(
                            self.propiedad_id),
                        'portales@appto.co',
                        [publicacion2.agente.email],
                        fail_silently=False,
                    )

                    publicacion = PublicacionComercial.objects.get(propiedad=self.propiedad,
                                                                   estado=PublicacionComercial.ESTADO_PUBLICADO,
                                                                   tipo_negocio=self.tipo_negocio)
                    cliente = None
                    try:
                        cliente = Cliente.objects.get(email=self.email)

                        necesidad = None
                        try:
                            necesidad = Necesidad.objects.get(cliente=cliente, activo=True)
                        except Necesidad.DoesNotExist:
                            necesidad = Necesidad.objects.create(cliente=cliente,
                                                                 precio_min=publicacion.precio * decimal.Decimal(0.8),
                                                                 precio_max=publicacion.precio * decimal.Decimal(1.2),
                                                                 area_min=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                     0.8),
                                                                 area_max=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                     1.2),
                                                                 tipo_negocio=publicacion.tipo_negocio,
                                                                 notas=self.mensaje_usuario,
                                                                 habitaciones_min=publicacion.propiedad.espacios,
                                                                 parqueaderos_min=publicacion.propiedad.estacionamientos_totales,
                                                                 banos_min=publicacion.propiedad.banos,
                                                                 propiedad_primer_contacto=self.propiedad,
                                                                 activo=True)

                        PropiedadNecesidad.objects.create(necesidad=necesidad,
                                                          publicacion=publicacion,
                                                          valor_propiedad_inicial=publicacion.precio, )


                    except Cliente.DoesNotExist:
                        cliente = Cliente.objects.create(nombre=self.nombre, apellido=self.apellido,
                                                         nacionalidad='Colombia',
                                                         email=self.email, telefono_principal=self.telefono)

                        necesidad = Necesidad.objects.create(cliente=cliente,
                                                             precio_min=publicacion.precio * decimal.Decimal(0.8),
                                                             precio_max=publicacion.precio * decimal.Decimal(1.2),
                                                             area_min=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                 0.8),
                                                             area_max=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                 1.2),
                                                             tipo_negocio=publicacion.tipo_negocio,
                                                             notas=self.mensaje_usuario,
                                                             habitaciones_min=publicacion.propiedad.espacios,
                                                             parqueaderos_min=publicacion.propiedad.estacionamientos_totales,
                                                             banos_min=publicacion.propiedad.banos,
                                                             propiedad_primer_contacto=self.propiedad,
                                                             activo=True)

                        PropiedadNecesidad.objects.create(necesidad=necesidad,
                                                          publicacion=publicacion,
                                                          valor_propiedad_inicial=publicacion.precio, )

            # except PublicacionComercial.DoesNotExist:
            except:
                pass

            # Publicación Industrial
            try:
                with transaction.atomic():
                    publicacion2 = PublicacionIndustrial.objects.get(propiedad=self.propiedad,
                                                                     estado=PublicacionIndustrial.ESTADO_PUBLICADO)
                    send_mail(
                        'Tienes un nuevo contacto portales',
                        'Tienes un nuevo contacto que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + str(
                            self.propiedad_id),
                        'portales@appto.co',
                        [publicacion2.agente.email],
                        fail_silently=False,
                    )

                    publicacion = PublicacionIndustrial.objects.get(propiedad=self.propiedad,
                                                                    estado=PublicacionIndustrial.ESTADO_PUBLICADO,
                                                                    tipo_negocio=self.tipo_negocio)
                    cliente = None
                    try:
                        cliente = Cliente.objects.get(email=self.email)

                        necesidad = None
                        try:
                            necesidad = Necesidad.objects.get(cliente=cliente, activo=True)
                        except Necesidad.DoesNotExist:
                            necesidad = Necesidad.objects.create(cliente=cliente,
                                                                 precio_min=publicacion.precio * decimal.Decimal(
                                                                     0.8),
                                                                 precio_max=publicacion.precio * decimal.Decimal(
                                                                     1.2),
                                                                 area_min=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                     0.8),
                                                                 area_max=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                     1.2),
                                                                 tipo_negocio=publicacion.tipo_negocio,
                                                                 notas=self.mensaje_usuario,
                                                                 habitaciones_min=publicacion.propiedad.espacios,
                                                                 parqueaderos_min=0,
                                                                 banos_min=publicacion.propiedad.banos,
                                                                 propiedad_primer_contacto=self.propiedad,
                                                                 activo=True)

                        PropiedadNecesidad.objects.create(necesidad=necesidad,
                                                          publicacion=publicacion,
                                                          valor_propiedad_inicial=publicacion.precio, )


                    except Cliente.DoesNotExist:
                        cliente = Cliente.objects.create(nombre=self.nombre, apellido=self.apellido,
                                                         nacionalidad='Colombia',
                                                         email=self.email, telefono_principal=self.telefono)

                        necesidad = Necesidad.objects.create(cliente=cliente,
                                                             precio_min=publicacion.precio * decimal.Decimal(0.8),
                                                             precio_max=publicacion.precio * decimal.Decimal(1.2),
                                                             area_min=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                 0.8),
                                                             area_max=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                 1.2),
                                                             tipo_negocio=publicacion.tipo_negocio,
                                                             notas=self.mensaje_usuario,
                                                             habitaciones_min=publicacion.propiedad.espacios,
                                                             parqueaderos_min=0,
                                                             banos_min=publicacion.propiedad.banos,
                                                             propiedad_primer_contacto=self.propiedad,
                                                             activo=True)

                        PropiedadNecesidad.objects.create(necesidad=necesidad,
                                                          publicacion=publicacion,
                                                          valor_propiedad_inicial=publicacion.precio, )
            # except PublicacionComercial.DoesNotExist:
            except:
                pass

            # Publicación Lotes
            try:
                with transaction.atomic():
                    publicacion2 = PublicacionLotes.objects.get(propiedad=self.propiedad,
                                                                estado=PublicacionLotes.ESTADO_PUBLICADO)
                    send_mail(
                        'Tienes un nuevo contacto portales',
                        'Tienes un nuevo contacto que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + str(
                            self.propiedad_id),
                        'portales@appto.co',
                        [publicacion2.agente.email],
                        fail_silently=False,
                    )

                    publicacion = PublicacionLotes.objects.get(propiedad=self.propiedad,
                                                               estado=PublicacionLotes.ESTADO_PUBLICADO,
                                                               tipo_negocio=self.tipo_negocio)
                    cliente = None
                    try:
                        cliente = Cliente.objects.get(email=self.email)

                        necesidad = None
                        try:
                            necesidad = Necesidad.objects.get(cliente=cliente, activo=True)
                        except Necesidad.DoesNotExist:
                            necesidad = Necesidad.objects.create(cliente=cliente,
                                                                 precio_min=publicacion.precio * decimal.Decimal(
                                                                     0.8),
                                                                 precio_max=publicacion.precio * decimal.Decimal(
                                                                     1.2),
                                                                 area_min=publicacion.propiedad.area_lote * decimal.Decimal(
                                                                     0.8),
                                                                 area_max=publicacion.propiedad.area_lote * decimal.Decimal(
                                                                     1.2),
                                                                 tipo_negocio=publicacion.tipo_negocio,
                                                                 notas=self.mensaje_usuario,
                                                                 habitaciones_min=0,
                                                                 parqueaderos_min=0,
                                                                 banos_min=0,
                                                                 propiedad_primer_contacto=self.propiedad,
                                                                 activo=True)

                        PropiedadNecesidad.objects.create(necesidad=necesidad,
                                                          publicacion=publicacion,
                                                          valor_propiedad_inicial=publicacion.precio, )


                    except Cliente.DoesNotExist:
                        cliente = Cliente.objects.create(nombre=self.nombre, apellido=self.apellido,
                                                         nacionalidad='Colombia',
                                                         email=self.email, telefono_principal=self.telefono)

                        necesidad = Necesidad.objects.create(cliente=cliente,
                                                             precio_min=publicacion.precio * decimal.Decimal(0.8),
                                                             precio_max=publicacion.precio * decimal.Decimal(1.2),
                                                             area_min=publicacion.propiedad.area_lote * decimal.Decimal(
                                                                 0.8),
                                                             area_max=publicacion.propiedad.area_lote * decimal.Decimal(
                                                                 1.2),
                                                             tipo_negocio=publicacion.tipo_negocio,
                                                             notas=self.mensaje_usuario,
                                                             habitaciones_min=0,
                                                             parqueaderos_min=0,
                                                             banos_min=0,
                                                             propiedad_primer_contacto=self.propiedad,
                                                             activo=True)

                        PropiedadNecesidad.objects.create(necesidad=necesidad,
                                                          publicacion=publicacion,
                                                          valor_propiedad_inicial=publicacion.precio, )
            # except PublicacionComercial.DoesNotExist:
            except:
                pass

            self.ha_creado_sol_contacto = True
        super(ContactoPortales, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Contacto portales'
        verbose_name_plural = 'Contacto portales'


class ContactoPagina(models.Model):
    propiedad = models.ForeignKey(Propiedad, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(null=True, blank=True, max_length=120)
    apellido = models.CharField(null=True, blank=True, max_length=120)
    telefono = models.CharField(null=True, blank=True, max_length=30)
    email = models.EmailField(null=True, blank=True)
    ha_creado_sol_contacto = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    ESTADOS_CREADO_POR_WEB = 0
    ESTADOS_TRAMITADO = 1
    ESTADOS_CORREO_NO_APLICA = 3
    ESTADOS_NO_INTERESA = 4

    ESTADOS = (
        (ESTADOS_CREADO_POR_WEB, 'Creado por web'),
        (ESTADOS_TRAMITADO, 'Requerimiento CREADO'),
        (ESTADOS_CORREO_NO_APLICA, 'Correo no aplica para requerimiento'),
        (ESTADOS_NO_INTERESA, 'No interesa'),
    )
    estado = models.IntegerField(null=False, choices=ESTADOS, default=ESTADOS_CREADO_POR_WEB)

    def __str__(self):
        return str(self.estado) + ' ' + str(self.fecha_creacion) + ' ' + str(self.nombre) + ' - ' + str(self.apellido)

        # def save(self, *args, **kwargs):

        # +++++++++++++++++++++++++++

    def save(self, *args, **kwargs):
        from slacker import Slacker

        if self.estado == ContactoPagina.ESTADOS_CREADO_POR_WEB:
            try:
                publicacion2 = PublicacionVivienda.objects.get(propiedad=self.propiedad,
                                                               estado=PublicacionVivienda.ESTADO_PUBLICADO)
                send_mail(
                    'Tienes un nuevo contacto',
                    'Tienes un nuevo contacto que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + str(
                        self.propiedad_id) + '. Por favor ve al CRM para hacer matching a este contacto.',
                    'portales@appto.co',
                    [publicacion2.agente.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionComercial.objects.get(propiedad=self.propiedad,
                                                                estado=PublicacionComercial.ESTADO_PUBLICADO)
                send_mail(
                    'Tienes un nuevo contacto',
                    'Tienes un nuevo contacto que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + self.propiedad_id + '. Por favor ve al CRM para hacer matching a este contacto.',
                    'portales@appto.co',
                    [publicacion2.agente.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionIndustrial.objects.get(propiedad=self.propiedad,
                                                                 estado=PublicacionIndustrial.ESTADO_PUBLICADO)
                send_mail(
                    'Tienes un nuevo contacto',
                    'Tienes un nuevo contacto que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + publicacion2.propiedad_id + '. Por favor ve al CRM para hacer matching a este contacto.',
                    'portales@appto.co',
                    [publicacion2.agente.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionLotes.objects.get(propiedad=self.propiedad,
                                                            estado=PublicacionLotes.ESTADO_PUBLICADO)
                send_mail(
                    'Tienes un nuevo contacto',
                    'Tienes un nuevo contacto que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + publicacion2.propiedad_id + '. Por favor ve al CRM para hacer matching a este contacto.',
                    'portales@appto.co',
                    [publicacion2.agente.email],
                    fail_silently=False,
                )
            except:
                pass

        # ++++++++++++++++++++++++++++

        if not self.ha_creado_sol_contacto:

            # Publicación vivienda
            try:
                publicacion = PublicacionVivienda.objects.get(propiedad=self.propiedad,
                                                              estado=PublicacionVivienda.ESTADO_PUBLICADO)
                cliente = None
                try:
                    cliente = Cliente.objects.get(email=self.email)

                    necesidad = None
                    try:
                        necesidad = Necesidad.objects.get(cliente=cliente, activo=True)
                    except Necesidad.DoesNotExist:
                        necesidad = Necesidad.objects.create(cliente=cliente,
                                                             precio_min=publicacion.precio * decimal.Decimal(0.8),
                                                             precio_max=publicacion.precio * decimal.Decimal(1.2),
                                                             area_min=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                 0.8),
                                                             area_max=publicacion.propiedad.area_construida * decimal.Decimal(
                                                                 1.2),
                                                             tipo_negocio=publicacion.tipo_negocio,
                                                             habitaciones_min=publicacion.propiedad.habitaciones,
                                                             parqueaderos_min=publicacion.propiedad.estacionamientos_totales,
                                                             banos_min=publicacion.propiedad.banos,
                                                             propiedad_primer_contacto=self.propiedad,
                                                             activo=True)

                    PropiedadNecesidad.objects.create(necesidad=necesidad,
                                                      publicacion=publicacion,
                                                      valor_propiedad_inicial=publicacion.precio, )


                except Cliente.DoesNotExist:
                    cliente = Cliente.objects.create(nombre=self.nombre, apellido=self.apellido,
                                                     nacionalidad='Colombia',
                                                     email=self.email, telefono_principal=self.telefono,
                                                     agente_id=publicacion.agente.id)

                    necesidad = Necesidad.objects.create(cliente=cliente,
                                                         precio_min=publicacion.precio * decimal.Decimal(0.8),
                                                         precio_max=publicacion.precio * decimal.Decimal(1.2),
                                                         area_min=publicacion.propiedad.area_construida * decimal.Decimal(
                                                             0.8),
                                                         area_max=publicacion.propiedad.area_construida * decimal.Decimal(
                                                             1.2),
                                                         tipo_negocio=publicacion.tipo_negocio,
                                                         habitaciones_min=publicacion.propiedad.habitaciones,
                                                         parqueaderos_min=publicacion.propiedad.estacionamientos_totales,
                                                         banos_min=publicacion.propiedad.banos,
                                                         propiedad_primer_contacto=self.propiedad,
                                                         activo=True)

                    PropiedadNecesidad.objects.create(necesidad=necesidad,
                                                      publicacion=publicacion,
                                                      valor_propiedad_inicial=publicacion.precio, )

            except PublicacionVivienda.DoesNotExist:
                pass

            self.ha_creado_sol_contacto = True
        super(ContactoPagina, self).save(*args, **kwargs)


# ************************************************************
# Esta clase maneja los contactos de los cursos
# ContactoCurso
# ************************************************************
class ContactoCurso(models.Model):
    ESTADOS_CREADO_POR_WEB = 0
    ESTADOS_TRAMITADO = 1
    ESTADOS_FINALIZADO = 3
    ESTADOS_NO_INTERESA = 4

    ESTADOS = (
        (ESTADOS_CREADO_POR_WEB, 'Creado por web'),
        (ESTADOS_TRAMITADO, 'Tramitado por Operaciones'),
        (ESTADOS_FINALIZADO, 'Finalizado'),
        (ESTADOS_NO_INTERESA, 'No interesa'),
    )
    estado = models.IntegerField(null=False, choices=ESTADOS, default=ESTADOS_CREADO_POR_WEB)

    nombre = models.CharField(null=True, blank=True, max_length=120)
    apellido = models.CharField(null=True, blank=True, max_length=120)
    telefono = models.CharField(null=True, blank=True, max_length=30)
    email = models.EmailField(null=False, blank=False)

    CIUDADES_BOGOTA = 0
    # CIUDADES_BARRANQUILLA = 1

    CIUDADES = (
        (CIUDADES_BOGOTA, 'Bogotá'),
        # (CIUDADES_BARRANQUILLA, 'Barranquilla'),
    )
    ciudad = models.IntegerField(null=False, choices=CIUDADES, default=CIUDADES_BOGOTA)

    CURSO_1 = 0
    # MODO_TRABAJO_INMOBILIARIA = 1
    # MODO_TRABAJO_OTRO = 2

    CURSO = (
        (CURSO_1, 'Gestión Comercial y Estrategias Inmobiliarias'),
        # (MODO_TRABAJO_INMOBILIARIA, 'Trabajo con Inmobiliaria'),
        # (MODO_TRABAJO_OTRO, 'Otro'),
    )
    curso = models.IntegerField(null=False, choices=CURSO, default=CURSO_1)

    comentarios = models.TextField(null=True, blank=True)

    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return str(self.fecha_creacion) + ' ' + str(self.nombre) + ' - ' + str(self.apellido)

    def save(self, *args, **kwargs):
        from slacker import Slacker

        if self.estado == ContactoCurso.ESTADOS_CREADO_POR_WEB:
            try:
                slack = Slacker('xoxb-43612317654-UnhAHi6ajw0bmmfxmHHee6J6')
                slack.chat.post_message(channel='#candidatos',
                                        text='Tenemos un nuevo candidato: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + '',
                                        username="crm")
            except:
                pass

        super(ContactoCurso, self).save(*args, **kwargs)


# ************************************************************
# Esta clase maneja las citas
# ContactoCita
# ************************************************************
class ContactoCita(models.Model):
    agente = models.ForeignKey(Agente, null=True, blank=True, on_delete=models.CASCADE)
    propiedad = models.ForeignKey(Propiedad, null=True, blank=True, on_delete=models.CASCADE)

    ESTADOS_CREADO_POR_WEB = 0
    ESTADOS_TRAMITADO = 1
    ESTADOS_FINALIZADO = 2
    ESTADOS_NO_INTERESA = 3

    ESTADOS = (
        (ESTADOS_CREADO_POR_WEB, 'Creado por web'),
        (ESTADOS_TRAMITADO, 'Tramitado'),
        (ESTADOS_FINALIZADO, 'Finalizado'),
        (ESTADOS_NO_INTERESA, 'No interesa'),
    )
    estado = models.IntegerField(null=False, choices=ESTADOS, default=ESTADOS_CREADO_POR_WEB)

    nombre = models.CharField(null=True, blank=True, max_length=120)
    apellido = models.CharField(null=True, blank=True, max_length=120)
    telefono = models.CharField(null=True, blank=True, max_length=30)
    email = models.EmailField(null=False, blank=False)

    comentarios = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)
    fecha_agenda = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.fecha_creacion) + ' ' + str(self.nombre) + ' - ' + str(self.apellido)

    def save(self, *args, **kwargs):
        from slacker import Slacker

        if self.estado == ContactoCita.ESTADOS_CREADO_POR_WEB:
            try:
                slack = Slacker('xoxb-43612317654-UnhAHi6ajw0bmmfxmHHee6J6')
                slack.chat.post_message(channel='#consignaciones',
                                        text='Tenemos una nueva cita de ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + '',
                                        username="crm")
            except:
                pass

        # Creados por web
        if self.estado == ContactoCita.ESTADOS_CREADO_POR_WEB:
            try:
                publicacion2 = PublicacionVivienda.objects.get(propiedad=self.propiedad,
                                                               estado=PublicacionVivienda.ESTADO_PUBLICADO)
                send_mail(
                    'Tienes una nueva cita',
                    'Tienes una nueva cita que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita:  ' + str(formats.date_format(self.fecha_agenda,
                                                                                                "SHORT_DATETIME_FORMAT")) + '. Por favor ve al CRM mirar el detalle en Agendas.',
                    'portales@appto.co',
                    [publicacion2.agente.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionComercial.objects.get(propiedad=self.propiedad,
                                                                estado=PublicacionComercial.ESTADO_PUBLICADO)
                send_mail(
                    'Tienes una nueva cita',
                    'Tienes una nueva cita que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita:  ' + str(formats.date_format(self.fecha_agenda,
                                                                                                "SHORT_DATETIME_FORMAT")) + '. Por favor ve al CRM mirar el detalle en Agendas.',
                    'portales@appto.co',
                    [publicacion2.agente.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionIndustrial.objects.get(propiedad=self.propiedad,
                                                                 estado=PublicacionIndustrial.ESTADO_PUBLICADO)
                send_mail(
                    'Tienes una nueva cita',
                    'Tienes una nueva cita que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita:  ' + str(formats.date_format(self.fecha_agenda,
                                                                                                "SHORT_DATETIME_FORMAT")) + '. Por favor ve al CRM mirar el detalle en Agendas.',
                    'portales@appto.co',
                    [publicacion2.agente.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionLotes.objects.get(propiedad=self.propiedad,
                                                            estado=PublicacionLotes.ESTADO_PUBLICADO)
                send_mail(
                    'Tienes una nueva cita',
                    'Tienes una nueva cita que necesita de tu colaboración: ' + self.nombre + ' ' + self.apellido + '. Teléfono: ' + self.telefono + ' E-mail: ' + self.email + ' El código del inmueble por el que entro es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita:  ' + str(formats.date_format(self.fecha_agenda,
                                                                                                "SHORT_DATETIME_FORMAT")) + '. Por favor ve al CRM mirar el detalle en Agendas.',
                    'portales@appto.co',
                    [publicacion2.agente.email],
                    fail_silently=False,
                )
            except:
                pass

        # Tramitados
        if self.estado == ContactoCita.ESTADOS_TRAMITADO:
            try:
                publicacion2 = PublicacionVivienda.objects.get(propiedad=self.propiedad,
                                                               estado=PublicacionVivienda.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita fue aceptada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionComercial.objects.get(propiedad=self.propiedad,
                                                                estado=PublicacionComercial.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita fue aceptada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionIndustrial.objects.get(propiedad=self.propiedad,
                                                                 estado=PublicacionIndustrial.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita fue aceptada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionLotes.objects.get(propiedad=self.propiedad,
                                                            estado=PublicacionLotes.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita fue aceptada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

        # Finalizado
        if self.estado == ContactoCita.ESTADOS_FINALIZADO:
            try:
                publicacion2 = PublicacionVivienda.objects.get(propiedad=self.propiedad,
                                                               estado=PublicacionVivienda.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita fue finalizada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita fue:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionComercial.objects.get(propiedad=self.propiedad,
                                                                estado=PublicacionComercial.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita fue finalizada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita fue:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionIndustrial.objects.get(propiedad=self.propiedad,
                                                                 estado=PublicacionIndustrial.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita fue finalizada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita fue:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionLotes.objects.get(propiedad=self.propiedad,
                                                            estado=PublicacionLotes.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita fue finalizada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita fue:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

        # Rechazada
        if self.estado == ContactoCita.ESTADOS_NO_INTERESA:
            try:
                publicacion2 = PublicacionVivienda.objects.get(propiedad=self.propiedad,
                                                               estado=PublicacionVivienda.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita no fue aceptada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita fue:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionComercial.objects.get(propiedad=self.propiedad,
                                                                estado=PublicacionComercial.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita no fue aceptada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita fue:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionIndustrial.objects.get(propiedad=self.propiedad,
                                                                 estado=PublicacionIndustrial.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita no fue aceptada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita fue:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

            try:
                publicacion2 = PublicacionLotes.objects.get(propiedad=self.propiedad,
                                                            estado=PublicacionLotes.ESTADO_PUBLICADO)
                send_mail(
                    'Respuesta de tu cita inmobiliaria Appto',
                    'Tu cita no fue aceptada: ' + '. Teléfono agente: ' + publicacion2.agente.telefono_contacto + ' E-mail agente: ' + publicacion2.agente.email + ' El código del inmueble es: ' + str(
                        self.propiedad_id) + ' - Fecha de la cita fue:  ' + str(
                        formats.date_format(self.fecha_agenda, "SHORT_DATETIME_FORMAT")) + '.',
                    'portales@appto.co',
                    [self.email],
                    fail_silently=False,
                )
            except:
                pass

        super(ContactoCita, self).save(*args, **kwargs)
