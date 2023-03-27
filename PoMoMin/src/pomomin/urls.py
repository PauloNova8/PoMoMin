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

from inventario.views import *
from empleados.views import *
from sucursales.views import *
from fabricantes.views import *
from proveedores.views import *
from bitacora.views import *
from usuarios.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('login/iniciarSesion/', login, name='iniciarSesion'),
    path('logout/', kill_session, name='logout'),

    path('asignarInventario/', inventario_buscar_view, name='asignarInventario'),
    path('asignarInventario/cargarInventario/', cargar_inventario, name='cargarInventario'),
    path('asignarInventario/cargarEmpleado/', cargar_empleado, name='cargarEmpleado'),
    path('asignarInventario/asignar/', asignar, name='asignar'),

    path('desasignarInventario/', inventario_desasignacion_buscar_view, name='desasignarInventario'),
    path('desasignarInventario/cargarInventario/', cargar_inventario_desasignar, name='desCargarInventario'),
    path('desasignarInventario/cargarEmpleado/', cargar_empleado_desasignar, name='descargarEmpleado'),
    path('desasignarInventario/cargarFecha/', cargar_fecha_asignacion, name='cargarFecha'),
    path('desasignarInventario/desasignar/', desasignar, name='desasignar'),

    
    path('registrarEquipo/', equipo_insert_view, name='registrarEquipo'),
    path('registrarEquipo/equipoInsertar/', sp_insertar_equipo, name='sp_insertar_equipo'),
    path('buscarEquipo/', equipo_buscar_view, name='buscarEquipo'),
    path('buscarEquipo/actualizar/<int:id>', equipo_actualizar_view, name='actualizarEquipo'),
    path('buscarEquipo/actualizar/equipoActualizar/', sp_actualizar_equipo, name='sp_actualizar_equipo'),
    path('buscarEquipo/actualizar/equipoDesactivar/', sp_desactivar_equipo, name='sp_desactivar_equipo'),
    path('registrarEquipo/codigoBarras/', generar_codigo_barras, name='generar_ebarras'),
    path('registrarEquipo/codigoQR/', generar_codigo_qr, name='generar_eqr'),


    path('buscarEquipo/reporte/', r_equipo_actual_view, name='reporteEquipo'),
    path('buscarEquipo/reporteSucursal/', r_equipo_sucursal_view, name='reporteEquipoSucursal'),
    path('buscarMobiliario/reporte/', r_mobiliario_actual_view, name='reporteMobiliario'),
    path('buscarMobiliario/reporteSucursal/', r_mobiliario_sucursal_view, name='reporteMobiliarioSucursal'),
    path('buscarHistorico/reporte/', r_historico_view, name='reporteHistorico'),
    path('asignarInventario/reporte/', r_asignacion_view, name='reporteAsignacion'),

    
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


    path('registrarSucursal/', sucursal_insert_view, name='registrarSucursal'),
    path('registrarSucursal/sucursalInsertar/', sp_insertar_sucursal, name='sp_insertar_sucursal'),
    path('buscarSucursal/', sucursal_buscar_view, name='buscarSucursal'),
    path('buscarSucursal/actualizar/<int:id>', sucursal_actualizar_view, name='actualizarSucursal'),
    path('buscarSucursal/actualizar/sucursalActualizar/', sp_actualizar_sucursal, name='sp_actualizar_sucursal'),
    path('buscarSucursal/actualizar/sucursalDesactivar/', sp_desactivar_sucursal, name='sp_desactivar_sucursal'),


    path('registrarFabricante/', fabricante_insert_view, name='registrarFabricante'),
    path('registrarFabricante/fabricanteInsertar/', sp_insertar_fabricante, name='sp_insertar_fabricante'),
    path('buscarFabricante/', fabricante_buscar_view, name='buscarFabricante'),
    path('buscarFabricante/actualizar/<int:id>', fabricante_actualizar_view, name='actualizarFabricante'),
    path('buscarFabricante/actualizar/fabricanteActualizar/', sp_actualizar_fabricante, name='sp_actualizar_fabricante'),
    path('buscarFabricante/actualizar/fabricanteDesactivar/', sp_desactivar_fabricante, name='sp_desactivar_fabricante'),


    path('registrarProveedor/', proveedor_insert_view, name='registrarProveedor'),
    path('registrarProveedor/proveedorInsertar/', sp_insertar_proveedor, name='sp_insertar_proveedor'),
    path('buscarProveedor/', proveedor_buscar_view, name='buscarProveedor'),
    path('buscarProveedor/actualizar/<int:id>', proveedor_actualizar_view, name='actualizarProveedor'),
    path('buscarProveedor/actualizar/proveedorActualizar/', sp_actualizar_proveedor, name='sp_actualizar_proveedor'),
    path('buscarProveedor/actualizar/proveedorDesactivar/', sp_desactivar_proveedor, name='sp_desactivar_proveedor'),

    path('buscarBitacora/', bitacora_buscar_view, name='buscarBitacora'),
    path('buscarBitacora/verRegistro/<int:id>', bitacora_detalles_view, name='verBitacora'),

    path('buscarHistorico/', historico_buscar_view, name='buscarHistorico'),
    path('buscarHistorico/verHistorico/<int:id>', historico_detalles_view, name='verHistorico'),
    

    path('registrarUsuario/', usuario_insert_view, name='registrarUsuario'),
    path('registrarUsuario/usuarioInsertar/', sp_insertar_usuario, name='sp_insertar_usuario'),
    path('buscarUsuario/', usuario_buscar_view, name='buscarUsuario'),
    path('buscarUsuario/actualizar/<int:id>', usuario_actualizar_view, name='actualizarUsuario'),
    path('buscarUsuario/actualizar/usuarioActualizar/', sp_actualizar_usuario, name='sp_actualizar_usuario'),
    path('buscarUsuario/actualizar/usuarioDesactivar/', sp_desactivar_usuario, name='sp_desactivar_usuario'),


    path('admin/', admin.site.urls),
]
