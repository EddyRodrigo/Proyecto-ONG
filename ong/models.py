from django.db import models
from typing import Any
from django.db.models.manager import Manager


class Voluntario(models.Model):
    id_voluntario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    rol = models.CharField(max_length=100, null=True, blank=True)
    ci = models.CharField(max_length=20, null=True, blank=True)
    correo = models.CharField(max_length=150, null=True, blank=True)
    horas_acumuladas = models.IntegerField(default=0)

    objects: Manager[Any] = models.Manager()

    class Meta:
        managed = False
        db_table = 'voluntarios'


class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True)
    nombre_evento = models.CharField(max_length=200, null=True, blank=True)
    proposito = models.TextField(null=True, blank=True)
    fecha_evento = models.DateField(null=True, blank=True)

    objects: Manager[Any] = models.Manager()

    class Meta:
        managed = False
        db_table = 'eventos'


class Inscrito(models.Model):
    id_inscrito = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    ci = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    objects: Manager[Any] = models.Manager()

    class Meta:
        managed = False
        db_table = 'inscritos'


class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        db_column='id_evento',
        related_name='asistencias',
        null=True,
        blank=True
    )
    voluntario = models.ForeignKey(
        Voluntario,
        on_delete=models.CASCADE,
        db_column='id_voluntario',
        related_name='asistencias',
        null=True,
        blank=True
    )
    inscrito = models.ForeignKey(
        Inscrito,
        on_delete=models.CASCADE,
        db_column='id_inscrito',
        related_name='asistencias',
        null=True,
        blank=True
    )
    hora_llegada = models.DateTimeField(null=True, blank=True)
    hora_salida = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'asistencia'
