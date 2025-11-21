
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
#* Importamos las views  de la app ong
from ong import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #* Definimos la ruta principal para que apunte a la vista home de la app ong
    path('', views.home, name='home'),
    path('ong/', include('ong.urls')),

]
