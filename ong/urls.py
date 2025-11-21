from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from ong import views




urlpatterns = [

    # -------- VOLUNTARIOS --------
    path('voluntarios/', views.listar_voluntarios, name='listar_voluntarios'),
    path('voluntarios/agregar/', views.guardar_voluntario, name='agregar_voluntario'),
    path('voluntarios/editar/<int:id_voluntario>/', views.actualizar_voluntario, name='editar_voluntario'),
    path('voluntarios/eliminar/<int:id_voluntario>/', views.eliminar_voluntario, name='eliminar_voluntario'),

    # -------- INSCRITOS --------
    path('inscritos/', views.listar_inscritos, name='listar_inscritos'),
    path('inscritos/agregar/', views.guardar_inscrito, name='agregar_inscrito'),
    path('inscritos/editar/<int:id_inscrito>/', views.actualizar_inscrito, name='editar_inscrito'),
    path('inscritos/eliminar/<int:id_inscrito>/', views.eliminar_inscrito, name='eliminar_inscrito'),

    # -------- EVENTOS --------
    path('eventos/', views.listar_eventos, name='listar_eventos'),
    path('eventos/agregar/', views.guardar_evento, name='agregar_evento'),
    path('eventos/editar/<int:id_evento>/', views.actualizar_evento, name='editar_evento'),
    path('eventos/eliminar/<int:id_evento>/', views.eliminar_evento, name='eliminar_evento'),

    # -------- ASISTENCIA --------
    path('asistencias/', views.listar_asistencias, name='listar_asistencias'),
    path('asistencias/agregar/', views.guardar_asistencia, name='agregar_asistencia'),
    path('asistencias/editar/<int:id_asistencia>/', views.actualizar_asistencia, name='editar_asistencia'),
    path('asistencias/eliminar/<int:id_asistencia>/', views.eliminar_asistencia, name='eliminar_asistencia'),

    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
