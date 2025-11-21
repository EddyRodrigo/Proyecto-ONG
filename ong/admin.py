from django.contrib import admin
from .models import Voluntario, Inscrito, Evento, Asistencia


# -------------------------------
#* VOLUNTARIOS
# -------------------------------
@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ('id_voluntario', 'nombre', 'apellido', 'rol', 'ci', 'correo', 'horas_acumuladas')
    search_fields = ('nombre', 'apellido', 'ci', 'rol')
    list_filter = ('rol',)
    ordering = ('id_voluntario',)


# -------------------------------
#* INSCRITOS
# -------------------------------
@admin.register(Inscrito)
class InscritoAdmin(admin.ModelAdmin):
    list_display = ('id_inscrito', 'nombre', 'apellido', 'ci', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'ci')
    ordering = ('id_inscrito',)


# -------------------------------
#* EVENTOS
# -------------------------------
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id_evento', 'nombre_evento', 'proposito', 'fecha_evento')
    search_fields = ('nombre_evento', 'proposito')
    list_filter = ('fecha_evento',)
    ordering = ('id_evento',)


# -------------------------------
#* ASISTENCIA
# -------------------------------
@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = (
        'id_asistencia',
        'evento_nombre',
        'voluntario_nombre',
        'inscrito_nombre',
        'hora_llegada',
        'hora_salida'
    )

    search_fields = (
        'evento__nombre_evento',
        'voluntario__nombre',
        'voluntario__apellido',
        'inscrito__nombre',
        'inscrito__apellido',
    )

    list_filter = ('hora_llegada', 'hora_salida')

    ordering = ('id_asistencia',)


#* ----- Columnas personalizadas -----  en ves del "Evento object (X)"

    def evento_nombre(self, obj):
        return obj.evento.nombre_evento if obj.evento else '—'
    evento_nombre.short_description = "Evento"

    def voluntario_nombre(self, obj):
        if obj.voluntario:
            return f"{obj.voluntario.nombre} {obj.voluntario.apellido}"
        return '—'
    voluntario_nombre.short_description = "Voluntario"

    def inscrito_nombre(self, obj):
        if obj.inscrito:
            return f"{obj.inscrito.nombre} {obj.inscrito.apellido}"
        return '—'
    inscrito_nombre.short_description = "Inscrito"
