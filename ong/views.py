from django.shortcuts import render, redirect, get_object_or_404
from .models import Voluntario, Inscrito, Evento, Asistencia
from datetime import datetime

from datetime import datetime
from django.db import transaction

def _compute_hours(start, end):
    if not start or not end:
        return 0.0

    if isinstance(start, str):
        
        #? año - mes - dia  | hora - min
        try:
            start = datetime.fromisoformat(start)
        except ValueError:
            start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")

    if isinstance(end, str):
        try:
            end = datetime.fromisoformat(end)
        except ValueError:
            end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

    delta = end - start
    hours = delta.total_seconds() / 3600.0
    #* REdondear al + Cercano  
    #! Tratar de mostrar todo
    return hours




#* pagina principal
def home(request):
    return render(request, 'home.html')
# --------------------------------------------------------
#* CRUD VOLUNTARIO
# --------------------------------------------------------

def listar_voluntarios(request):
    voluntarios = Voluntario.objects.all()
    return render(request, 'voluntarios/listar_voluntarios.html', {'voluntarios': voluntarios})


def guardar_voluntario(request):
    if request.method == 'POST':
        Voluntario.objects.create(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            rol=request.POST['rol'],
            ci=request.POST['ci'],
            correo=request.POST['correo']
        )
        return redirect('listar_voluntarios')
    return render(request, 'voluntarios/agregar_voluntario.html')


def actualizar_voluntario(request, id_voluntario):
    voluntario = get_object_or_404(Voluntario, id_voluntario=id_voluntario)

    if request.method == 'POST':
        voluntario.nombre = request.POST['nombre']
        voluntario.apellido = request.POST['apellido']
        voluntario.rol = request.POST['rol']
        voluntario.ci = request.POST['ci']
        voluntario.correo = request.POST['correo']
        voluntario.save()
        return redirect('listar_voluntarios')

    return render(request, 'voluntarios/actualizar_voluntario.html', {'voluntario': voluntario})


def eliminar_voluntario(request, id_voluntario):
    voluntario = get_object_or_404(Voluntario, id_voluntario=id_voluntario)
    voluntario.delete()
    return redirect('listar_voluntarios')



# --------------------------------------------------------
#* CRUD INSCRITO
# --------------------------------------------------------

def listar_inscritos(request):
    inscritos = Inscrito.objects.all()
    return render(request, 'inscritos/listar_inscritos.html', {'inscritos': inscritos})


def guardar_inscrito(request):
    if request.method == 'POST':
        Inscrito.objects.create(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            ci=request.POST['ci'],
            fecha_nacimiento=request.POST['fecha_nacimiento']
        )
        return redirect('listar_inscritos')

    return render(request, 'inscritos/agregar_inscrito.html')


def actualizar_inscrito(request, id_inscrito):
    inscrito = get_object_or_404(Inscrito, id_inscrito=id_inscrito)

    if request.method == 'POST':
        inscrito.nombre = request.POST['nombre']
        inscrito.apellido = request.POST['apellido']
        inscrito.ci = request.POST['ci']
        inscrito.fecha_nacimiento = request.POST['fecha_nacimiento']
        inscrito.save()
        return redirect('listar_inscritos')

    return render(request, 'inscritos/actualizar_inscrito.html', {'inscrito': inscrito})


def eliminar_inscrito(request, id_inscrito):
    inscrito = get_object_or_404(Inscrito, id_inscrito=id_inscrito)
    inscrito.delete()
    return redirect('listar_inscritos')



# --------------------------------------------------------
#* CRUD EVENTO
# --------------------------------------------------------

def listar_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/listar_eventos.html', {'eventos': eventos})


def guardar_evento(request):
    if request.method == 'POST':
        Evento.objects.create(
            nombre_evento=request.POST['nombre_evento'],
            proposito=request.POST['proposito'],
            fecha_evento=request.POST['fecha_evento']
        )
        return redirect('listar_eventos')

    return render(request, 'eventos/agregar_evento.html')


def actualizar_evento(request, id_evento):
    evento = get_object_or_404(Evento, id_evento=id_evento)

    if request.method == 'POST':
        evento.nombre_evento = request.POST['nombre_evento']
        evento.proposito = request.POST['proposito']
        evento.fecha_evento = request.POST['fecha_evento']
        evento.save()
        return redirect('listar_eventos')

    return render(request, 'eventos/actualizar_evento.html', {'evento': evento})


def eliminar_evento(request, id_evento):
    evento = get_object_or_404(Evento, id_evento=id_evento)
    evento.delete()
    return redirect('listar_eventos')



# --------------------------------------------------------
#* CRUD ASISTENCIA
# --------------------------------------------------------

def listar_asistencias(request):
    asistencias = Asistencia.objects.all()
    return render(request, 'asistencias/listar_asistencias.html', {'asistencias': asistencias})


def guardar_asistencia(request):
    if request.method == 'POST':
        evento_id = request.POST.get('evento')
        voluntario_id = request.POST.get('voluntario') or None
        inscrito_id = request.POST.get('inscrito') or None
        hora_llegada = request.POST.get('hora_llegada')
        hora_salida = request.POST.get('hora_salida')

        with transaction.atomic():
            asistencia = Asistencia.objects.create(
                evento_id=evento_id,
                voluntario_id=voluntario_id,
                inscrito_id=inscrito_id,
                hora_llegada=hora_llegada,
                hora_salida=hora_salida
            )

            #* si es voluntario ir a sumar sus horas a la tabla voluntario
            if asistencia.voluntario:
                horas = _compute_hours(asistencia.hora_llegada, asistencia.hora_salida)
                asistencia.voluntario.horas_acumuladas = int(round(asistencia.voluntario.horas_acumuladas + horas))
                asistencia.voluntario.save()

        return redirect('listar_asistencias')

    eventos = Evento.objects.all()
    voluntarios = Voluntario.objects.all()
    inscritos = Inscrito.objects.all()

    return render(request, 'asistencias/agregar_asistencia.html', {
        'eventos': eventos,
        'voluntarios': voluntarios,
        'inscritos': inscritos
    })



def actualizar_asistencia(request, id_asistencia):
    asistencia = get_object_or_404(Asistencia, id_asistencia=id_asistencia)

    #* Guardamos una copia antes de guardar los cambios
    prev_vol = asistencia.voluntario
    prev_lleg = asistencia.hora_llegada
    prev_sali = asistencia.hora_salida

    if request.method == 'POST':
        #* Nuevos valores del formulario
        new_evento = request.POST.get('evento')
        new_voluntario = request.POST.get('voluntario') or None
        new_inscrito = request.POST.get('inscrito') or None
        new_llegada = request.POST.get('hora_llegada')
        new_salida = request.POST.get('hora_salida')

        with transaction.atomic():

            #*revertimos horas anteriores si había voluntario
            if prev_vol:
                horas_previas = _compute_hours(prev_lleg, prev_sali)
                prev_vol.horas_acumuladas = int(round(prev_vol.horas_acumuladas - horas_previas))
                if prev_vol.horas_acumuladas < 0:
                    prev_vol.horas_acumuladas = 0
                prev_vol.save()

            #* Actualizamos asistencia
            asistencia.evento_id = new_evento
            asistencia.voluntario_id = new_voluntario
            asistencia.inscrito_id = new_inscrito
            asistencia.hora_llegada = new_llegada
            asistencia.hora_salida = new_salida
            asistencia.save()

            #* Ahora sumamos horas nuevas al nuevo voluntario
            if asistencia.voluntario:
                horas_nuevas = _compute_hours(asistencia.hora_llegada, asistencia.hora_salida)
                asistencia.voluntario.horas_acumuladas = int(round(asistencia.voluntario.horas_acumuladas + horas_nuevas))
                asistencia.voluntario.save()

        return redirect('listar_asistencias')

    #TODO: Datos para el formulario
    eventos = Evento.objects.all()
    voluntarios = Voluntario.objects.all()
    inscritos = Inscrito.objects.all()

    return render(request, 'asistencias/actualizar_asistencia.html', {
        'asistencia': asistencia,
        'eventos': eventos,
        'voluntarios': voluntarios,
        'inscritos': inscritos
    })



def eliminar_asistencia(request, id_asistencia):
    asistencia = get_object_or_404(Asistencia, id_asistencia=id_asistencia)

    # TODO: Si tenía voluntario, restar horas antes de eliminar
    if asistencia.voluntario:
        horas_previas = _compute_hours(asistencia.hora_llegada, asistencia.hora_salida)
        asistencia.voluntario.horas_acumuladas -= int(round(horas_previas))
        if asistencia.voluntario.horas_acumuladas < 0:
            asistencia.voluntario.horas_acumuladas = 0
        asistencia.voluntario.save()

    asistencia.delete()
    return redirect('listar_asistencias')


