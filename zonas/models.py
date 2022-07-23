from django.db import models


# Create your models here.
class Zona(models.Model):
    TIPOS_ZONA = (
        ('pais', 'País'),
        ('ciudad', 'Ciudad'),
        ('upz', 'UPZ'),
        ('appto', 'Zona Appto'),
    )

    tipo_zona = models.CharField(max_length=32, choices=TIPOS_ZONA)
    slug = models.SlugField(unique=True, null=False, blank=False, max_length=100)
    nombre = models.CharField(null=False, blank=False, max_length=80)

    def __str__(self):
        return str(self.nombre)


# ************************************************************
# Esta clase maneja los Departamentos
# Municipio
# ************************************************************
class Departamento(models.Model):
    codigo = models.CharField(null=True, blank=True, max_length=10)
    nombre = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Departamentos"
        verbose_name = "Departamento"


# ************************************************************
# Esta clase maneja los municipios
# Municipios
# ************************************************************
class Municipio(models.Model):
    codigo = models.CharField(null=True, blank=True, max_length=10)
    nombre = models.CharField(null=True, blank=True, max_length=255)
    departamento = models.ForeignKey(Departamento, verbose_name='Departamento', on_delete=models.CASCADE)
    activo = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.nombre + ' - ' + self.departamento.nombre

    class Meta:
        verbose_name_plural = "Municipios"
        verbose_name = "Municipio"
