from django.shortcuts import render, redirect, get_object_or_404
from .models import Voluntario, Inscrito, Evento, Asistencia
from datetime import datetime






def home(request):
    return render(request, 'home.html')
# --------------------------------------------------------
# CRUD VOLUNTARIO
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
# CRUD INSCRITO
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
# CRUD EVENTO
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
# CRUD ASISTENCIA
# --------------------------------------------------------

def listar_asistencias(request):
    asistencias = Asistencia.objects.all()
    return render(request, 'asistencias/listar_asistencias.html', {'asistencias': asistencias})


def guardar_asistencia(request):
    if request.method == 'POST':
        Asistencia.objects.create(
            evento_id=request.POST['evento'],
            voluntario_id=request.POST['voluntario'] if request.POST['voluntario'] else None,
            inscrito_id=request.POST['inscrito'] if request.POST['inscrito'] else None,
            hora_llegada=request.POST['hora_llegada'],
            hora_salida=request.POST['hora_salida']
        )
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

    if request.method == 'POST':
        asistencia.evento_id = request.POST['evento']
        asistencia.voluntario_id = request.POST['voluntario'] or None
        asistencia.inscrito_id = request.POST['inscrito'] or None
        asistencia.hora_llegada = request.POST['hora_llegada']
        asistencia.hora_salida = request.POST['hora_salida']
        asistencia.save()
        return redirect('listar_asistencias')

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
    asistencia.delete()
    return redirect('listar_asistencias')

