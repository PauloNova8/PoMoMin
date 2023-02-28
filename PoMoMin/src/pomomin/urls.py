"""pomomin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from inventario.views import equipo_insert_view
from inventario.views import sp_insertar_equipo
from inventario.views import equipo_buscar_view
from inventario.views import equipo_actualizar_view
from inventario.views import sp_actualizar_equipo
from inventario.views import sp_desactivar_equipo
from inventario.views import generar_codigo_barras
from inventario.views import generar_codigo_qr
from inventario.views import escaner_view

from inventario.views import mobiliario_insert_view
from inventario.views import sp_insertar_mobiliario
from inventario.views import mobiliario_buscar_view
from inventario.views import mobiliario_actualizar_view
from inventario.views import sp_actualizar_mobiliario
from inventario.views import sp_desactivar_mobiliario

from empleados.views import empleado_insert_view
from empleados.views import sp_insertar_empleado
from empleados.views import cargar_puestos
from empleados.views import cargar_jefes
from empleados.views import empleado_buscar_view
from empleados.views import empleado_actualizar_view
from empleados.views import sp_actualizar_empleado
from empleados.views import sp_desactivar_empleado

urlpatterns = [
    path('', escaner_view, name='home'),
    
    path('registrarEquipo/', equipo_insert_view, name='registrarEquipo'),
    path('registrarEquipo/equipoInsertar/', sp_insertar_equipo, name='sp_insertar_equipo'),
    path('buscarEquipo/', equipo_buscar_view, name='buscarEquipo'),
    path('buscarEquipo/actualizar/<int:id>', equipo_actualizar_view, name='actualizarEquipo'),
    path('buscarEquipo/actualizar/equipoActualizar/', sp_actualizar_equipo, name='sp_actualizar_equipo'),
    path('buscarEquipo/actualizar/equipoDesactivar/', sp_desactivar_equipo, name='sp_desactivar_equipo'),
    path('registrarEquipo/codigoBarras/', generar_codigo_barras, name='generar_ebarras'),
    path('registrarEquipo/codigoQR/', generar_codigo_qr, name='generar_eqr'),

    
    path('registrarMobiliario/', mobiliario_insert_view, name='registrarMobiliario'),
    path('registrarMobiliario/mobiliarioInsertar/', sp_insertar_mobiliario, name='sp_insertar_mobiliario'),
    path('buscarMobiliario/', mobiliario_buscar_view, name='buscarMobiliario'),
    path('buscarMobiliario/actualizar/<int:id>', mobiliario_actualizar_view, name='actualizarMobiliario'),
    path('buscarMobiliario/actualizar/mobiliarioActualizar/', sp_actualizar_mobiliario, name='sp_actualizar_mobiliario'),
    path('buscarMobiliario/actualizar/mobiliarioDesactivar/', sp_desactivar_mobiliario, name='sp_desactivar_mobiliario'),
    path('registrarMobiliario/codigoBarras/', generar_codigo_barras, name='generar_ebarras'),
    path('registrarMobiliario/codigoQR/', generar_codigo_qr, name='generar_eqr'),


    path('registrarEmpleado/', empleado_insert_view, name='registrarEmpleado'),
    path('registrarEmpleado/cargarPuestos/', cargar_puestos, name='puestos'),
    path('registrarEmpleado/cargarJefes/', cargar_jefes, name='jefes'),
    path('registrarEmpleado/empleadoInsertar/', sp_insertar_empleado, name='sp_insertar_empleado'),
    path('buscarEmpleado/', empleado_buscar_view, name='buscarEmpleado'),
    path('buscarEmpleado/actualizar/<int:id>', empleado_actualizar_view, name='actualizarEmpleado'),
    path('buscarEmpleado/actualizar/cargarPuestos/', cargar_puestos, name='Apuestos'),
    path('buscarEmpleado/actualizar/cargarJefes/', cargar_jefes, name='Ajefes'),
    path('buscarEmpleado/actualizar/empleadoActualizar/', sp_actualizar_empleado, name='sp_actualizar_empleado'),
    path('buscarEmpleado/actualizar/empleadoDesactivar/', sp_desactivar_empleado, name='sp_desactivar_empleado'),

    path('admin/', admin.site.urls),
]
