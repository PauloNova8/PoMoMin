from django.shortcuts import redirect, render
from django.utils import timezone
from .models import *
from usuarios.models import showUsuarios
from usuarios.views import login_view
from empleados.models import *
from usuarios.models import showUsuarios
from django.db import connection
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from dateutil import parser
from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.platypus import Paragraph, Table, TableStyle, Image, Spacer, SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib.units import cm
import datetime
import qrcode
from django.views.decorators.cache import cache_control

# EQUIPO
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def equipo_insert_view(request, *args, **kwargs):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1: 
        return redirect(login_view)
    else:
        if request.session.get('PerfilID', '') == 3: 
            return redirect(home_view)
        
        queryCategorias = "SELECT 1 AS id, CategoriaID, Categoria FROM Categorias WHERE AplicaA = 'E'"
        categorias = showCategorias.objects.raw(queryCategorias)

        queryFabricantes = "SELECT 1 AS id, FabricanteID, Nombre FROM Fabricantes WHERE Activo = 1"
        fabricantes = showFabricantes.objects.raw(queryFabricantes)

        queryEstados = "SELECT 1 AS id, EstadoID, Estado FROM EstadosInventario"
        estados = showEstados.objects.raw(queryEstados)

        querySucursales = "SELECT 1 AS id, SucursalID, Nombre FROM Sucursales WHERE Activo = 1"
        sucursales = showSucursales.objects.raw(querySucursales)

        queryProveedores = "SELECT 1 AS id, ProveedorID, Nombre FROM Proveedores WHERE Activo = 1"
        proveedores = showProveedores.objects.raw(queryProveedores)

        context = {
            "showCategorias": categorias,
            "showFabricantes": fabricantes,
            "showEstados": estados,
            "showSucursales": sucursales,
            "showProveedores": proveedores,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'insertarEquipo.html', context)

def sp_insertar_equipo(request):
    if request.method == 'POST':
        try:
            conteo = 0
            fechaSoporte = request.POST['FechaUltimoSoporte']
            if(request.POST['FechaUltimoSoporte'] == ''):
                fechaSoporte = None
            descripcion = request.POST['Descripcion']
            if(request.POST['Descripcion'] == ''):
                descripcion = None
            notas = request.POST['Notas']
            if(request.POST['Notas'] == ''):
                notas = None
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @ID AS INT;
                                    EXEC INSERT_INVENTARIO %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, @ID = @ID OUTPUT
                                    SELECT @ID AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  request.POST['CodigoInventario'], request.POST['CodigoBarra'], int(request.POST['TipoInventarioID']),
                            int(request.POST['CategoriaID']), int(request.POST['FabricanteID']), request.POST['Modelo'], request.POST['Serie'], 
                            descripcion, int(request.POST['SucursalID']), int(request.POST['ProveedorID']), int(request.POST['EstadoID']), 
                            request.POST['FechaCompra'], None, fechaSoporte, 
                            notas, request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Ha devuelto un error.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def equipo_buscar_view(request, *args, **kwargs):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        queryInventario = """SELECT * FROM v_Inventario WHERE TipoInventarioID = 1"""
        inventario = showInventario.objects.raw(queryInventario)
        context = {
            "showInventario": inventario,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'buscarEquipo.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def equipo_actualizar_view(request, id):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        if request.session.get('PerfilID', '') == 3: 
            return redirect(home_view)
        
        queryInventario = """SELECT * FROM v_Inventario WHERE InventarioID = %s"""
        inventarios = showInventario.objects.raw(queryInventario, [int(id)])

        queryCategorias = "SELECT 1 AS id, CategoriaID, Categoria FROM Categorias WHERE AplicaA = 'E'"
        categorias = showCategorias.objects.raw(queryCategorias)

        queryFabricantes = "SELECT 1 AS id, FabricanteID, Nombre, Activo FROM Fabricantes ORDER BY Activo DESC"
        fabricantes = showFabricantes.objects.raw(queryFabricantes)

        queryEstados = "SELECT 1 AS id, EstadoID, Estado FROM EstadosInventario"
        estados = showEstados.objects.raw(queryEstados)

        querySucursales = "SELECT 1 AS id, SucursalID, Nombre, Activo FROM Sucursales ORDER BY Activo DESC"
        sucursales = showSucursales.objects.raw(querySucursales)

        queryProveedores = "SELECT 1 AS id, ProveedorID, Nombre,Activo FROM Proveedores ORDER BY Activo DESC"
        proveedores = showProveedores.objects.raw(queryProveedores)


        for obj in inventarios:
            inventario = obj
        
        obj.FechaCompra = parser.parse(str(obj.FechaCompra))
        if(obj.FechaUltimoSoporte != None):
            obj.FechaUltimoSoporte = parser.parse(str(obj.FechaUltimoSoporte))

        if(obj.Descripcion == None):
            obj.Descripcion = ""
        
        if(obj.Notas == None):
            obj.Notas = ""

        if(obj.CodigoBarra[0] == 'B'):
            my_code = Code128(str(obj.CodigoBarra), writer=ImageWriter())
            my_code.save("static/codes/Cod-" + str(obj.CodigoBarra), options={"write_text": False})
        else:
            img = qrcode.make(obj.CodigoBarra)
            img.save("static/codes/Cod-" + str(obj.CodigoBarra) + ".png")

        if obj.AsignadoA is None:
            fechaVigente = None
        with connection.cursor() as cursor:
                query ='''SET NOCOUNT ON;
                        SELECT CAST(CONVERT(DATE, FechaVigente, 101) AS VARCHAR(30)) AS FechaVigente
                    FROM InventarioEmpleados
                    WHERE InventarioID = %s AND EmpleadoID = %s AND FechaFin IS NULL'''
                params = (  obj.InventarioID, obj.AsignadoA )
                cursor.execute(query, params)
                registro = cursor.fetchall()
                    
                for row in registro:
                    fechaVigente = str(row[0])
                    

        context = {
            "showCategorias": categorias,
            "showFabricantes": fabricantes,
            "showEstados": estados,
            "showSucursales": sucursales,
            "showProveedores": proveedores,
            "inventarioTraido": inventario,
            "fechaVigente": fechaVigente,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'actualizarEquipo.html', context)

def sp_actualizar_equipo(request):
    if request.method == 'POST':
        try:
            conteo = 0
            fechaSoporte = request.POST['FechaUltimoSoporte']
            if(request.POST['FechaUltimoSoporte'] == ''):
                fechaSoporte = None
            descripcion = request.POST['Descripcion']
            if(request.POST['Descripcion'] == ''):
                descripcion = None
            notas = request.POST['Notas']
            if(request.POST['Notas'] == ''):
                notas = None
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC UPDATE_INVENTARIO %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['InventarioID']), request.POST['CodigoInventario'],
                            int(request.POST['CategoriaID']), int(request.POST['FabricanteID']), request.POST['Modelo'], request.POST['Serie'], 
                            descripcion, int(request.POST['SucursalID']), int(request.POST['ProveedorID']), int(request.POST['EstadoID']), 
                            request.POST['FechaCompra'], None, fechaSoporte, 
                            notas, request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Ha devuelto un error.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
    
def sp_desactivar_equipo(request):
    if request.method == 'POST':
        try:
            conteo = 0
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC DEACTIVATE_INVENTARIO %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['InventarioID']), 2, request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Ha devuelto un error.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()



# MOBILIARIO
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mobiliario_insert_view(request, *args, **kwargs):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        if request.session.get('PerfilID', '') == 3: 
            return redirect(home_view)
        
        queryCategorias = "SELECT 1 AS id, CategoriaID, Categoria FROM Categorias WHERE AplicaA = 'M'"
        categorias = showCategorias.objects.raw(queryCategorias)

        queryFabricantes = "SELECT 1 AS id, FabricanteID, Nombre FROM Fabricantes WHERE Activo = 1"
        fabricantes = showFabricantes.objects.raw(queryFabricantes)

        queryEstados = "SELECT 1 AS id, EstadoID, Estado FROM EstadosInventario WHERE EstadoID <> 3"
        estados = showEstados.objects.raw(queryEstados)

        querySucursales = "SELECT 1 AS id, SucursalID, Nombre FROM Sucursales WHERE Activo = 1"
        sucursales = showSucursales.objects.raw(querySucursales)

        queryProveedores = "SELECT 1 AS id, ProveedorID, Nombre FROM Proveedores WHERE Activo = 1"
        proveedores = showProveedores.objects.raw(queryProveedores)

        context = {
            "showCategorias": categorias,
            "showFabricantes": fabricantes,
            "showEstados": estados,
            "showSucursales": sucursales,
            "showProveedores": proveedores,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'insertarMobiliario.html', context)

def sp_insertar_mobiliario(request):
    if request.method == 'POST':
        try:
            conteo = 0
            fechaUtil = request.POST['FechaUtilMaxima']
            if(request.POST['FechaUtilMaxima'] == ''):
                fechaUtil = None
            descripcion = request.POST['Descripcion']
            if(request.POST['Descripcion'] == ''):
                descripcion = None
            notas = request.POST['Notas']
            if(request.POST['Notas'] == ''):
                notas = None
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @ID AS INT;
                                    EXEC INSERT_INVENTARIO %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, @ID = @ID OUTPUT
                                    SELECT @ID AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  request.POST['CodigoInventario'], request.POST['CodigoBarra'], int(request.POST['TipoInventarioID']),
                            int(request.POST['CategoriaID']), int(request.POST['FabricanteID']), None, None, 
                            descripcion, int(request.POST['SucursalID']), int(request.POST['ProveedorID']), int(request.POST['EstadoID']), 
                            request.POST['FechaCompra'], fechaUtil, None, 
                            notas, request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Ha devuelto error.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mobiliario_buscar_view(request, *args, **kwargs):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        queryInventario = """SELECT * FROM v_Inventario WHERE TipoInventarioID = 2"""
        inventario = showInventario.objects.raw(queryInventario)
        context = {
            "showInventario": inventario,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'buscarMobiliario.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mobiliario_actualizar_view(request, id):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        if request.session.get('PerfilID', '') == 3: 
            return redirect(home_view)
        
        queryInventario = """SELECT * FROM v_Inventario WHERE InventarioID = %s"""
        inventarios = showInventario.objects.raw(queryInventario, [int(id)])

        queryCategorias = "SELECT 1 AS id, CategoriaID, Categoria FROM Categorias WHERE AplicaA = 'M'"
        categorias = showCategorias.objects.raw(queryCategorias)

        queryFabricantes = "SELECT 1 AS id, FabricanteID, Nombre, Activo FROM Fabricantes ORDER BY Activo DESC"
        fabricantes = showFabricantes.objects.raw(queryFabricantes)

        queryEstados = "SELECT 1 AS id, EstadoID, Estado FROM EstadosInventario WHERE EstadoID <> 3"
        estados = showEstados.objects.raw(queryEstados)

        querySucursales = "SELECT 1 AS id, SucursalID, Nombre, Activo FROM Sucursales ORDER BY Activo DESC"
        sucursales = showSucursales.objects.raw(querySucursales)

        queryProveedores = "SELECT 1 AS id, ProveedorID, Nombre,Activo FROM Proveedores ORDER BY Activo DESC"
        proveedores = showProveedores.objects.raw(queryProveedores)

        for obj in inventarios:
            inventario = obj
        
        obj.FechaCompra = parser.parse(str(obj.FechaCompra))
        if(obj.FechaUtilMaxima != None):
            obj.FechaUtilMaxima = parser.parse(str(obj.FechaUtilMaxima))

        if(obj.Descripcion is None):
            obj.Descripcion = ""
        
        if(obj.Notas is None):
            obj.Notas = ""

        if(obj.CodigoBarra[0] == 'B'):
            my_code = Code128(str(obj.CodigoBarra), writer=ImageWriter())
            my_code.save("static/codes/Cod-" + str(obj.CodigoBarra), options={"write_text": False})
        else:
            img = qrcode.make(obj.CodigoBarra)
            img.save("static/codes/Cod-" + str(obj.CodigoBarra) + ".png")

        if obj.AsignadoA is None:
            fechaVigente = None
        with connection.cursor() as cursor:
                query ='''SET NOCOUNT ON;
                        SELECT CAST(CONVERT(DATE, FechaVigente, 101) AS VARCHAR(30)) AS FechaVigente
                    FROM InventarioEmpleados
                    WHERE InventarioID = %s AND EmpleadoID = %s AND FechaFin IS NULL'''
                params = (  obj.InventarioID, obj.AsignadoA )
                cursor.execute(query, params)
                registro = cursor.fetchall()
                    
                for row in registro:
                    fechaVigente = str(row[0])

        context = {
            "showCategorias": categorias,
            "showFabricantes": fabricantes,
            "showEstados": estados,
            "showSucursales": sucursales,
            "showProveedores": proveedores,
            "inventarioTraido": inventario,
            "fechaVigente": fechaVigente,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'actualizarMobiliario.html', context)

def sp_actualizar_mobiliario(request):
    if request.method == 'POST':
        try:
            conteo = 0
            fechaUtil = request.POST['FechaUtilMaxima']
            if(request.POST['FechaUtilMaxima'] == ''):
                fechaUtil = None
            descripcion = request.POST['Descripcion']
            if(request.POST['Descripcion'] == ''):
                descripcion = None
            notas = request.POST['Notas']
            if(request.POST['Notas'] == ''):
                notas = None
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC UPDATE_INVENTARIO %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['InventarioID']), request.POST['CodigoInventario'],
                            int(request.POST['CategoriaID']), int(request.POST['FabricanteID']), None, None, 
                            descripcion, int(request.POST['SucursalID']), int(request.POST['ProveedorID']), int(request.POST['EstadoID']), 
                            request.POST['FechaCompra'], fechaUtil, None, 
                            notas, request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Ha devuelto un error.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
    
def sp_desactivar_mobiliario(request):
    if request.method == 'POST':
        try:
            conteo = 0
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC DEACTIVATE_INVENTARIO %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['InventarioID']), 2, request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Ha devuelto un error.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()



# GENERAR CODIGOS
def generar_codigo_barras(request):
    if request.method == 'POST':
        try:
            codigoInventario = request.POST.get('CodigoInventario', '')
            codigoAlfanumérico = 'B' + str(codigoInventario)
            print(codigoAlfanumérico)
            existeCodigo = 0
            with connection.cursor() as cursor:
                query ='''SELECT COUNT(*) FROM Inventario WHERE CodigoInventario = %s'''
                params = {  str(request.POST['CodigoInventario']) }
                cursor.execute(query, params)

                existeCodigo = int(cursor.fetchone()[0])
                if existeCodigo == 0:
                    my_code = Code128(str(codigoAlfanumérico), writer=ImageWriter())
                    my_code.save("static/codes/Cod-" + str(codigoAlfanumérico), options={"write_text": False})

                    response = JsonResponse({'Estado':existeCodigo, 'Mensaje': 'El código no existe así que se generó'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':existeCodigo, 'Mensaje': 'El código ya existe así que no se generó.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()

def generar_codigo_qr(request):
    if request.method == 'POST':
        try:
            codigoInventario = request.POST.get('CodigoInventario', '')
            codigoAlfanumérico = 'QR' + str(codigoInventario)
            print(codigoAlfanumérico)
            existeCodigo = 0
            with connection.cursor() as cursor:
                query ='''SELECT COUNT(*) FROM Inventario WHERE CodigoInventario = %s'''
                params = {  str(request.POST['CodigoInventario']) }
                cursor.execute(query, params)

                existeCodigo = int(cursor.fetchone()[0])
                if existeCodigo == 0:
                    img = qrcode.make(codigoAlfanumérico)
                    img.save("static/codes/Cod-" + str(codigoAlfanumérico) + ".png")

                    response = JsonResponse({'Estado':existeCodigo, 'Mensaje': 'El código no existe así que se generó'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':existeCodigo, 'Mensaje': 'El código ya existe así que no se generó.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()


# ASIGNACION
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inventario_buscar_view(request, *args, **kwargs):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        if request.session.get('PerfilID', '') == 3: 
            return redirect(home_view)
        
        queryMotivos = "SELECT 1 AS id, * FROM MotivosCambio WHERE AplicaA = 'A'"
        motivos = showMotivos.objects.raw(queryMotivos)

        context = {
            "showMotivos": motivos,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'asignarInventario.html', context)

def cargar_inventario(request):
    if request.method == 'POST':
        try:
            codigo = request.POST.get('codigo', '')
            with connection.cursor() as cursor:
                query ='''SET NOCOUNT ON;
                          SELECT * FROM v_Inventario WHERE EstadoID = 1 AND (CodigoBarra = %s OR CodigoInventario = %s) AND AsignadoA IS NULL'''
                params = (  codigo, codigo)
                cursor.execute(query, params)
                inventario = cursor.fetchall()
                
                if sum(1 for result in inventario) == 0:
                        response = ""
                else:
                    response = ""
                    for row in inventario:
                        response += "<tr><td><input type='checkbox' onclick='detectCheckBox()' id='inventarioSeleccionado' name='inventarioSeleccionado' value='" + str(row[1]) + "'/></td>"
                        response += "<td>" + str(row[2]) + "</td>"
                        response += "<td>" + str(row[3]) + "</td>"
                        if int(row[10]) == 1:
                            response += "<td>" + str(row[4]) + " " + str(row[5])  + "</td>"
                        else:
                            response += "<td>" + str(row[11]) + "</td>"
                        response += "<td style='text-align: center;'>Sin asignar</td>"
                        response += "<td>" + str(row[13]) + "</td>"
                        response += "<td style='text-align: center;'>"
                        if int(row[17]) == 1:
                            response += "<span class='badge badge-success' style='background-color: #28a745; text-transform: initial; font-size: 95%; min-width: 75px; max-width: 80px;'>" + str(row[18]) + "</span></td></tr>"
                return HttpResponse(response)
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
    
def cargar_empleado(request):
    if request.method == 'POST':
        try:
            identidad = request.POST.get('identidad', '')
            with connection.cursor() as cursor:
                query ='''SET NOCOUNT ON;
                          SELECT * FROM v_Empleados WHERE EstadoID <> 2 AND Identificacion = %s'''
                params = {  str(identidad) }
                cursor.execute(query, params)
                empleado = cursor.fetchall()
                
                if sum(1 for result in empleado) == 0:
                        response = ""
                else:
                    response = ""
                    for row in empleado:
                        response += "<tr><td><input type='checkbox' onclick='detectCheckBoxE()' id='empleadoSeleccionado' name='empleadoSeleccionado' value='" + str(row[1]) + "'/></td>"
                        response += "<td>" + str(row[11]) + "</td>"
                        response += "<td>" + str(row[9]) + "</td>"
                        response += "<td>" + str(row[23]) + "</td>"
                        response += "<td>" + str(row[6]) + "</td>"
                        response += "<td>" + str(row[10]) + "</td>"
                        response += "<td style='text-align: center;'>"
                        if int(row[20]) == 1:
                            response += "<span class='badge badge-success' style='background-color: #28a745; text-transform: initial; font-size: 95%; min-width: 75px; max-width: 80px;'>" + str(row[21]) + "</span></td></tr>"
                        elif int(row[20]) == 3:
                            response += "<span class='badge badge-warning' style='background-color: #e7b63a; text-transform: initial; font-size: 95%; min-width: 75px; max-width: 80px;'>" + str(row[21]) + "</span></td></tr>"
                        elif int(row[20]) == 4:
                            response += "<span class='badge badge-warning' style='background-color: #b8daff; text-transform: initial; font-size: 95%; min-width: 75px; max-width: 80px;'>" + str(row[21]) + "</span></td></tr>"

                return HttpResponse(response)
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()

def asignar(request):
    if request.method == 'POST':
        try:
            conteo = 0
            notas = request.POST['Notas']
            if(request.POST['Notas'] == ''):
                notas = None
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC ASIGNAR_INVENTARIO %s, %s, %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['InventarioID']), int(request.POST['EmpleadoID']), int(request.POST['MotivoID']),
                            notas, request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Ha devuelto error.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
    

# DESASIGNACION
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inventario_desasignacion_buscar_view(request, *args, **kwargs):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        if request.session.get('PerfilID', '') == 3: 
            return redirect(home_view)
        
        queryMotivos = "SELECT 1 AS id, * FROM MotivosCambio WHERE AplicaA = 'D'"
        motivos = showMotivos.objects.raw(queryMotivos)

        context = {
            "showMotivos": motivos,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'desasignarInventario.html', context)

def cargar_inventario_desasignar(request):
    if request.method == 'POST':
        try:
            codigo = request.POST.get('codigo', '')
            with connection.cursor() as cursor:
                query ='''SET NOCOUNT ON;
                          SELECT * FROM v_Inventario WHERE EstadoID = 1 AND (CodigoBarra = %s OR CodigoInventario = %s) AND AsignadoA IS NOT NULL'''
                params = (  codigo, codigo)
                cursor.execute(query, params)
                inventario = cursor.fetchall()
                
                if sum(1 for result in inventario) == 0:
                        response = ""
                else:
                    response = ""
                    for row in inventario:
                        response += "<input type='hidden' id='AsignadoAID' value='" + str(row[14]) + "'/>"
                        response += "<tr><td><input type='checkbox' onclick='detectCheckBoxDes()' id='inventarioSeleccionado' name='inventarioSeleccionado' value='" + str(row[1]) + "'/></td>"
                        response += "<td>" + str(row[2]) + "</td>"
                        response += "<td>" + str(row[3]) + "</td>"
                        if int(row[10]) == 1:
                            response += "<td>" + str(row[4]) + " " + str(row[5])  + "</td>"
                        else:
                            response += "<td>" + str(row[11]) + "</td>"
                        response += "<td style='text-align: center;'>Ya Asignado</td>"
                        response += "<td>" + str(row[13]) + "</td>"
                        response += "<td style='text-align: center;'>"
                        if int(row[17]) == 1:
                            response += "<span class='badge badge-success' style='background-color: #28a745; text-transform: initial; font-size: 95%; min-width: 75px; max-width: 80px;'>" + str(row[18]) + "</span></td></tr>"
                return HttpResponse(response)
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
 
def cargar_empleado_desasignar(request):
    if request.method == 'POST':
        try:
            EmpleadoID = request.POST.get('EmpleadoID', '')
            with connection.cursor() as cursor:
                query ='''SET NOCOUNT ON;
                          SELECT * FROM v_Empleados WHERE EmpleadoID = %s'''
                params = {  int(EmpleadoID) }
                cursor.execute(query, params)
                empleado = cursor.fetchall()
                
                if sum(1 for result in empleado) == 0:
                        response = ""
                else:
                    response = ""
                    for row in empleado:
                        response += "<tr><td style='display: none;'><input type='checkbox' checked id='empleadoSeleccionado' name='empleadoSeleccionado' value='" + str(row[1]) + "'/></td>"
                        response += "<td>" + str(row[11]) + "</td>"
                        response += "<td>" + str(row[9]) + "</td>"
                        response += "<td>" + str(row[23]) + "</td>"
                        response += "<td>" + str(row[6]) + "</td>"
                        response += "<td>" + str(row[10]) + "</td>"
                        response += "<td style='text-align: center;'>"
                        if int(row[20]) == 1:
                            response += "<span class='badge badge-success' style='background-color: #28a745; text-transform: initial; font-size: 95%; min-width: 75px; max-width: 80px;'>" + str(row[21]) + "</span></td></tr>"
                        elif int(row[20]) == 3:
                            response += "<span class='badge badge-warning' style='background-color: #e7b63a; text-transform: initial; font-size: 95%; min-width: 75px; max-width: 80px;'>" + str(row[21]) + "</span></td></tr>"
                        elif int(row[20]) == 4:
                            response += "<span class='badge badge-warning' style='background-color: #b8daff; text-transform: initial; font-size: 95%; min-width: 75px; max-width: 80px;'>" + str(row[21]) + "</span></td></tr>"

                return HttpResponse(response)
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()

def cargar_fecha_asignacion(request):
    if request.method == 'POST':
        try:
            InventarioID = request.POST.get('InventarioID', '')
            EmpleadoID = request.POST.get('EmpleadoID', '')
            fechaVigente = ''
            with connection.cursor() as cursor:
                query ='''SET NOCOUNT ON;
                        SELECT CAST(CONVERT(DATE, FechaVigente, 101) AS VARCHAR(30)) AS FechaVigente
                        FROM InventarioEmpleados
                        WHERE InventarioID = %s AND EmpleadoID = %s AND FechaFin IS NULL'''
                params = (  int(InventarioID), int(EmpleadoID) )
                cursor.execute(query, params)
                registro = cursor.fetchall()
                for row in registro:
                    fechaVigente = str(row[0])
                
            return HttpResponse(fechaVigente)
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()

def desasignar(request):
    if request.method == 'POST':
        try:
            conteo = 0
            notas = request.POST['Notas']
            if(request.POST['Notas'] == ''):
                notas = None
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC DESASIGNAR_INVENTARIO %s, %s, %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['InventarioID']), int(request.POST['EmpleadoID']), int(request.POST['MotivoID']),
                            notas, request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Ha devuelto error.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
    


# HISTORICO

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def historico_buscar_view(request, *args, **kwargs):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        if request.session.get('PerfilID', '') == 3: 
            return redirect(home_view)
        
        queryHistorico = """SELECT * FROM v_HistoricoAsignaciones"""
        historico = showHistorico.objects.raw(queryHistorico)
        context = {
            "showHistorico": historico,
            "device": request.META.get('COMPUTERNAME', '')
        }
    
    return render(request, 'buscarHistorico.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def historico_detalles_view(request, id):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        if request.session.get('PerfilID', '') == 3: 
            return redirect(home_view)
        
        queryHistorico = """SELECT * FROM v_HistoricoAsignaciones WHERE id = %s"""
        historico = showHistorico.objects.raw(queryHistorico, [int(id)])

        for obj in historico:
            registro = obj
        
        obj.FechaVigente = parser.parse(str(obj.FechaVigente))
        if(obj.FechaFin != None):
            obj.FechaFin = parser.parse(str(obj.FechaFin))

        if(obj.Notas == None):
            obj.Notas = ""

        if(obj.MotivoDesasignacion == None):
            obj.MotivoDesasignacion = ""
        
        context = {
            "registroTraido": registro,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'verHistorico.html', context)



# GRAFICOS
# EQUIPO
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_view(request, *args, **kwargs):
    if request.POST.get('Usuario', '') != '':
        queryUsuario = """SELECT * FROM v_Usuarios WHERE Usuario = %s"""
        usuarios = showUsuarios.objects.raw(queryUsuario, [request.POST.get('Usuario', '')])

        for obj in usuarios:
            usuario = obj
    
        request.session['UsuarioID'] = usuario.UsuarioID
        request.session['Usuario'] = usuario.Usuario
        request.session['PerfilID'] = usuario.PerfilID
        request.session['EstadoID'] = usuario.EstadoID

    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        conteoEquipo = ''
        with connection.cursor() as cursor:
            query ='''SET NOCOUNT ON;
                    SELECT COUNT(*) FROM Inventario WHERE TipoInventarioID = 1 AND EstadoID = 1 AND AsignadoA IS NULL'''
            cursor.execute(query)
            registro = cursor.fetchall()
            for row in registro:
                conteoEquipo = str(row[0])

        conteoMobiliario = ''
        with connection.cursor() as cursor:
            query ='''SET NOCOUNT ON;
                    SELECT COUNT(*) FROM Inventario WHERE TipoInventarioID = 2 AND EstadoID = 1 AND AsignadoA IS NULL'''
            cursor.execute(query)
            registro = cursor.fetchall()
            for row in registro:
                conteoMobiliario = str(row[0])

        conteoSoporte = ''
        with connection.cursor() as cursor:
            query ='''SET NOCOUNT ON;
                    SELECT COUNT(*) FROM Inventario WHERE EstadoID = 3'''
            cursor.execute(query)
            registro = cursor.fetchall()
            for row in registro:
                conteoSoporte = str(row[0])

        conteoBajas = ''
        with connection.cursor() as cursor:
            query ='''SET NOCOUNT ON;
                    SELECT COUNT(*) FROM InventarioEmpleados 
                    WHERE MotivoDesasignacionID = 8 
                    AND DATEADD(dd, 0, DATEDIFF(dd, 0, FechaFin)) = DATEADD(dd, 0, DATEDIFF(dd, 0, GETDATE()))'''
            cursor.execute(query)
            registro = cursor.fetchall()
            for row in registro:
                conteoBajas = str(row[0])

        asignacionesSemanal = ""
        with connection.cursor() as cursor:
            query ='''SET NOCOUNT ON;
                    SELECT * FROM v_ReporteAsignacionesSemanal ORDER BY Fecha'''
            cursor.execute(query)
            registro = cursor.fetchall()
            for row in registro:
                asignacionesSemanal += "," + str(row[2])
        
        desasignacionesSemanal = ""
        with connection.cursor() as cursor:
            query ='''SET NOCOUNT ON;
                    SELECT * FROM v_ReporteDesasignacionesSemanal ORDER BY Fecha'''
            cursor.execute(query)
            registro = cursor.fetchall()
            for row in registro:
                desasignacionesSemanal += "," + str(row[2])

        estadoInventario = ""
        with connection.cursor() as cursor:
            query ='''SET NOCOUNT ON;
                    SELECT * FROM v_ReporteEstadoInventario'''
            cursor.execute(query)
            registro = cursor.fetchall()
            for row in registro:
                estadoInventario += "," + str(row[2])

        
        context = {
            "conteoEquipoDisponible": conteoEquipo,
            "conteoMobiliarioDisponible": conteoMobiliario,
            "conteoSoporte": conteoSoporte,
            "conteoBajas": conteoBajas,
            "asignacionesSemanal": asignacionesSemanal,
            "desasignacionesSemanal": desasignacionesSemanal,
            "estadoInventario": estadoInventario,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'index.html', context)




# REPORTES

def addPageNumber(canvas, doc):
    page_num = canvas.getPageNumber()
    text = "Pág. %s" % page_num
    canvas.setFont('Helvetica',9)
    canvas.drawRightString(20.5*cm, 1.5*cm, text)

fecha = timezone.now().strftime('%d-%m-%Y %H:%M')

my_image = Image('https://imagenesm.000webhostapp.com/logoTextAsideNoBack.png', 200, 81)
my_image.hAlign = 'LEFT'

stylesParraf = getSampleStyleSheet()
stylesParraf.add(ParagraphStyle(name='Normal_CENTER',
                          parent=stylesParraf['Normal'],
                          fontName='Helvetica',
                          wordWrap='LTR',
                          alignment=TA_CENTER,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          ))
stylesParraf.add(ParagraphStyle(name='Normal_RIGHT',
                          parent=stylesParraf['Normal'],
                          fontName='Helvetica',
                          wordWrap='LTR',
                          alignment=TA_RIGHT,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          ))
stylesParraf.add(ParagraphStyle(name='Normal_JUSTIFY',
                          parent=stylesParraf['Normal'],
                          fontName='Helvetica',
                          wordWrap='LTR',
                          leading = 24,
                          alignment=TA_JUSTIFY,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          ))
stylesParraf.add(ParagraphStyle(name='Title_RIGHT',
                          parent=stylesParraf['Title'],
                          alignment=TA_RIGHT,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          ))

styleHeader = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 20),
        ('VALIGN',(0, 0),(-1,-1),'MIDDLE'),
    ])
style = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.slategrey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.slategrey),
    ('INNERGRID', (0, 0), (-1, 0), 0.25, colors.white),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.slategrey),
    ('VALIGN',(0, 0),(-1,-1),'MIDDLE'),
])
styleFirmas = TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('VALIGN',(0, 0),(-1,-1),'MIDDLE'),
])
styleParrafo = ParagraphStyle(
        name='Normal',
        fontSize=8,
        alignment=TA_CENTER,
)

def r_equipo_actual_view(request):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        queryInventario = """SELECT * FROM v_Inventario WHERE TipoInventarioID = 1"""
        inventario = showInventario.objects.raw(queryInventario)
        if not inventario:
            data = [['Reporte vacío']]
            data.append(['No se encontraron resultados para el reporte'])
            table = Table(data, [19 * cm, 9.5 * cm],  repeatRows=1)
            table.setStyle(style)
        else:
            data = [['Código Alfanumérico','Categoría','Modelo','Serie','Sucursal','Asignado','Estado']]
            for obj in inventario:
                asignado = 'Ya asignado'
                if obj.AsignadoA is None:
                    asignado = 'Sin Asignar'
                lista = [str(obj.CodigoInventario),str(obj.Categoria),str(obj.Modelo),str(obj.Serie),str(obj.Sucursal),asignado,str(obj.Estado)]
                data.append(lista)
            table = Table(data, repeatRows=1)
            table.setStyle(style)

        fileName = 'Reporte de Equipo del ' + fecha + '.pdf'

        response = HttpResponse(content_type='application/pdf') 
        response['Content-Disposition'] = 'filename="' + fileName + '"'

        pdf = SimpleDocTemplate(
            response,
            pagesize=letter,
            rightMargin=0, leftMargin=0, topMargin=0.5 * cm, bottomMargin=1.5 * cm
        )

        pdf.title = "Reporte de equipo (" + fecha + ")"
        pdf.creator = "PoMoMin"
        pdf.author = "PoMoMin"
        
        titulo = Paragraph("Reporte de equipo", stylesParraf['Title_RIGHT'])
        usuario = Paragraph("<b>Reporte solicitado por usuario:</b> " + str(request.session.get('Usuario', '')), stylesParraf['Normal'])
        fechaBloque = Paragraph("<b>Fecha y hora:</b> " + fecha, stylesParraf['Normal_RIGHT'])

        dataHeader = [
            [my_image, titulo],
            [usuario, fechaBloque],
        ]
        
        tablaHeader = Table(dataHeader, [9.5 * cm, 9.5 * cm])
        tablaHeader.setStyle(styleHeader)

        elements = []
        elements.append(tablaHeader)
        elements.append(Spacer(1 * cm, 1 * cm))
        elements.append(table)

        pdf.build(elements, onFirstPage=addPageNumber, onLaterPages=addPageNumber)

        return response

def r_equipo_sucursal_view(request):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        queryInventario = """SELECT * FROM v_Inventario WHERE TipoInventarioID = 1 AND AsignadoA IS NOT NULL ORDER BY SucursalID"""
        inventario = showInventario.objects.raw(queryInventario)
        if not inventario:
            data = [['Reporte vacío']]
            data.append(['No se encontraron resultados para el reporte'])
            table = Table(data, [19 * cm, 9.5 * cm],  repeatRows=1)
            table.setStyle(style)
        else:
            data = [['Código del equipo','Categoría','No.Identidad','Nombre del empleado','Departamento','Sucursal']]
            for obj in inventario:
                queryEmpleados = """SELECT * FROM v_Empleados WHERE NombreCompleto = %s"""
                empleados = showEmpleados.objects.raw(queryEmpleados, [str(obj.AsignadoNombre)])
                empleadoIdentidad = ''
                empleadoDepartamento = ''
                for empleado in empleados:
                    empleadoIdentidad = empleado.Identificacion
                    empleadoDepartamento = empleado.Departamento

                lista = [str(obj.CodigoInventario),str(obj.Categoria),str(empleadoIdentidad),str(obj.AsignadoNombre),str(empleadoDepartamento),str(obj.Sucursal)]
                data.append(lista)
            table = Table(data, repeatRows=1)
            table.setStyle(style)

        fileName = 'Reporte Asignaciones de Equipo por Sucursal del ' + fecha + '.pdf'

        response = HttpResponse(content_type='application/pdf') 
        response['Content-Disposition'] = 'filename="' + fileName + '"'

        pdf = SimpleDocTemplate(
            response,
            pagesize=letter,
            rightMargin=0, leftMargin=0, topMargin=0.5 * cm, bottomMargin=1.5 * cm
        )

        pdf.title = "Reporte de asignaciones de equipo por sucursal (" + fecha + ")"
        pdf.creator = "PoMoMin"
        pdf.author = "PoMoMin"
        
        titulo = Paragraph("Reporte de equipos asignados por sucursal", stylesParraf['Title_RIGHT'])
        usuario = Paragraph("<b>Reporte solicitado por usuario:</b> " + str(request.session.get('Usuario', '')), stylesParraf['Normal'])
        fechaBloque = Paragraph("<b>Fecha y hora:</b> " + fecha, stylesParraf['Normal_RIGHT'])

        dataHeader = [
            [my_image, titulo],
            [usuario, fechaBloque],
        ]
        
        tablaHeader = Table(dataHeader, [9.5 * cm, 9.5 * cm])
        tablaHeader.setStyle(styleHeader)

        elements = []
        elements.append(tablaHeader)
        elements.append(Spacer(1 * cm, 1 * cm))
        elements.append(table)

        pdf.build(elements, onFirstPage=addPageNumber, onLaterPages=addPageNumber)

        return response

def r_mobiliario_actual_view(request):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        queryInventario = """SELECT * FROM v_Inventario WHERE TipoInventarioID = 2"""
        inventario = showInventario.objects.raw(queryInventario)

        if not inventario:
            data = [['Reporte vacío']]
            data.append(['No se encontraron resultados para el reporte'])
            table = Table(data, [19 * cm, 9.5 * cm],  repeatRows=1)
            table.setStyle(style)
        else:
            data = [['Código Alfanumérico','Categoría','Fabricante','Sucursal','Asignado','Estado']]
            for obj in inventario:
                asignado = 'Ya asignado'
                if obj.AsignadoA is None:
                    asignado = 'Sin Asignar'
                lista = [str(obj.CodigoInventario),str(obj.Categoria),str(obj.Fabricante),str(obj.Sucursal),asignado,str(obj.Estado)]
                data.append(lista)
            table = Table(data, colWidths=[5*cm, 2*cm, 3*cm, 4*cm, 2*cm, 3*cm], repeatRows=1)
            table.setStyle(style)

        fileName = 'Reporte de Mobiliario del ' + fecha + '.pdf'

        response = HttpResponse(content_type='application/pdf') 
        response['Content-Disposition'] = 'filename="' + fileName + '"'

        pdf = SimpleDocTemplate(
            response,
            pagesize=letter,
            rightMargin=0, leftMargin=0, topMargin=0.5 * cm, bottomMargin=1.5 * cm
        )

        pdf.title = "Reporte de mobiliario (" + fecha + ")"
        pdf.creator = "PoMoMin"
        pdf.author = "PoMoMin"
        
        titulo = Paragraph("Reporte de mobiliario", stylesParraf['Title_RIGHT'])
        usuario = Paragraph("<b>Reporte solicitado por usuario:</b> " + str(request.session.get('Usuario', '')), stylesParraf['Normal'])
        fechaBloque = Paragraph("<b>Fecha y hora:</b> " + fecha, stylesParraf['Normal_RIGHT'])

        dataHeader = [
            [my_image, titulo],
            [usuario, fechaBloque],
        ]
        
        tablaHeader = Table(dataHeader, [9.5 * cm, 9.5 * cm])
        tablaHeader.setStyle(styleHeader)

        elements = []
        elements.append(tablaHeader)
        elements.append(Spacer(1 * cm, 1 * cm))
        elements.append(table)

        pdf.build(elements, onFirstPage=addPageNumber, onLaterPages=addPageNumber)

        return response

def r_mobiliario_sucursal_view(request):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        queryInventario = """SELECT * FROM v_Inventario WHERE TipoInventarioID = 2 AND AsignadoA IS NOT NULL ORDER BY SucursalID"""
        inventario = showInventario.objects.raw(queryInventario)

        if not inventario:
            data = [['Reporte vacío']]
            data.append(['No se encontraron resultados para el reporte'])
            table = Table(data, [19 * cm, 9.5 * cm],  repeatRows=1)
            table.setStyle(style)
        else:
            data = [['Código del mobiliario','Categoría','No.Identidad','Nombre del empleado','Departamento','Sucursal']]
            for obj in inventario:
                queryEmpleados = """SELECT * FROM v_Empleados WHERE NombreCompleto = %s"""
                empleados = showEmpleados.objects.raw(queryEmpleados, [str(obj.AsignadoNombre)])
                empleadoIdentidad = ''
                empleadoDepartamento = ''
                for empleado in empleados:
                    empleadoIdentidad = empleado.Identificacion
                    empleadoDepartamento = empleado.Departamento

                lista = [str(obj.CodigoInventario),str(obj.Categoria),str(empleadoIdentidad),str(obj.AsignadoNombre),str(empleadoDepartamento),str(obj.Sucursal)]
                data.append(lista)
            table = Table(data, repeatRows=1)
            table.setStyle(style)

        fileName = 'Reporte Asignaciones de Mobiliario por Sucursal del ' + fecha + '.pdf'

        response = HttpResponse(content_type='application/pdf') 
        response['Content-Disposition'] = 'filename="' + fileName + '"'

        pdf = SimpleDocTemplate(
            response,
            pagesize=letter,
            rightMargin=0, leftMargin=0, topMargin=0.5 * cm, bottomMargin=1.5 * cm
        )

        pdf.title = "Reporte de asignaciones de mobiliario por sucursal (" + fecha + ")"
        pdf.creator = "PoMoMin"
        pdf.author = "PoMoMin"
        
        titulo = Paragraph("Reporte de mobiliario asignado por sucursal", stylesParraf['Title_RIGHT'])
        usuario = Paragraph("<b>Reporte solicitado por usuario:</b> " + str(request.session.get('Usuario', '')), stylesParraf['Normal'])
        fechaBloque = Paragraph("<b>Fecha y hora:</b> " + fecha, stylesParraf['Normal_RIGHT'])

        dataHeader = [
            [my_image, titulo],
            [usuario, fechaBloque],
        ]
        
        tablaHeader = Table(dataHeader, [9.5 * cm, 9.5 * cm])
        tablaHeader.setStyle(styleHeader)

        elements = []
        elements.append(tablaHeader)
        elements.append(Spacer(1 * cm, 1 * cm))
        elements.append(table)

        pdf.build(elements, onFirstPage=addPageNumber, onLaterPages=addPageNumber)

        return response

def r_historico_view(request):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        queryAsignaciones = """SELECT * FROM v_HistoricoAsignaciones WHERE MONTH(FechaVigente) = MONTH(GETDATE()) OR MONTH(FechaFin) = MONTH(GETDATE()) ORDER BY FechaVigente"""
        asignaciones = showHistorico.objects.raw(queryAsignaciones)

        if not asignaciones:
            data = [['Sin asignaciones de inventario en este mes']]
            data.append(['No se encontraron resultados para el reporte'])
            table = Table(data, [19 * cm, 9.5 * cm],  repeatRows=1)
            table.setStyle(style)
        else:
            data = [['Código del inventario','No.Identidad','Empleado','Tipo de cambio','Motivo de cambio','Fecha del cambio']]
            for obj in asignaciones:
                queryEmpleados = """SELECT * FROM v_Empleados WHERE CONCAT(Nombre, ' ', Apellido) = %s"""
                empleados = showEmpleados.objects.raw(queryEmpleados, [str(obj.NombreCompleto)])
                empleadoIdentidad = ''
                for empleado in empleados:
                    empleadoIdentidad = empleado.Identificacion

                if parser.parse(str(obj.FechaVigente)).month == datetime.date.today().month:
                    lista = [str(obj.CodigoInventario),str(empleadoIdentidad),str(obj.NombreCompleto),'Asignación',Paragraph(str(obj.MotivoAsignacion), style=styleParrafo),str(obj.FechaVigente.strftime('%d-%m-%Y %H:%M'))]
                    data.append(lista)
                if obj.FechaFin is not None:
                    if parser.parse(str(obj.FechaFin)).month == datetime.date.today().month:
                        lista = [str(obj.CodigoInventario),str(empleadoIdentidad),str(obj.NombreCompleto),'Desasignación',Paragraph(str(obj.MotivoDesasignacion), style=styleParrafo),str(obj.FechaFin.strftime('%d-%m-%Y %H:%M'))]
                        data.append(lista)
            table = Table(data, colWidths=[4*cm, 3*cm, 4*cm, 2.5*cm, 3*cm, 3*cm], repeatRows=1)
            table.setStyle(style)

        fileName = 'Informe de movimiento de inventario del mes (' + fecha + ').pdf'

        response = HttpResponse(content_type='application/pdf') 
        response['Content-Disposition'] = 'filename="' + fileName + '"'

        pdf = SimpleDocTemplate(
            response,
            pagesize=letter,
            rightMargin=0, leftMargin=0, topMargin=0.5 * cm, bottomMargin=1.5 * cm
        )

        pdf.title = "Informe de movimiento de inventario del mes (" + fecha + ")"
        pdf.creator = "PoMoMin"
        pdf.author = "PoMoMin"
        
        titulo = Paragraph("Informe de movimiento de inventario mensual", stylesParraf['Title_RIGHT'])
        usuario = Paragraph("<b>Reporte solicitado por usuario:</b> " + str(request.session.get('Usuario', '')), stylesParraf['Normal'])
        fechaBloque = Paragraph("<b>Fecha y hora:</b> " + fecha, stylesParraf['Normal_RIGHT'])

        dataHeader = [
            [my_image, titulo],
            [usuario, fechaBloque],
        ]
        
        tablaHeader = Table(dataHeader, [9.5 * cm, 9.5 * cm])
        tablaHeader.setStyle(styleHeader)

        elements = []
        elements.append(tablaHeader)
        elements.append(Spacer(1 * cm, 1 * cm))
        elements.append(table)

        pdf.build(elements, onFirstPage=addPageNumber, onLaterPages=addPageNumber)

        return response

def r_asignacion_view(request):
    if request.session.get('UsuarioID', None) is None:
        return redirect(login_view)
    
    queryUsuario = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
    usuarios = showUsuarios.objects.raw(queryUsuario, [request.session.get('UsuarioID', '')])
    for obj in usuarios:
        usuario = obj
    request.session['UsuarioID'] = usuario.UsuarioID
    request.session['Usuario'] = usuario.Usuario
    request.session['PerfilID'] = usuario.PerfilID
    request.session['EstadoID'] = usuario.EstadoID
    if request.session.get('EstadoID', '') != 1:
        return redirect(login_view)
    else:
        queryAsignaciones = """SELECT TOP 1 * FROM v_HistoricoAsignaciones WHERE FechaFin IS NULL ORDER BY FechaVigente DESC """
        asignaciones = showHistorico.objects.raw(queryAsignaciones)
        for asign in asignaciones:
            asignacion = asign
            InventarioID = asign.InventarioID
            EmpleadoID = asign.EmpleadoID

        queryInventario = """SELECT * FROM v_Inventario WHERE InventarioID = %s"""
        inventarios = showInventario.objects.raw(queryInventario, [InventarioID])
        for inven in inventarios:
            inventario = inven
        
        queryEmpleados = """SELECT * FROM v_Empleados WHERE EmpleadoID = %s"""
        empleados = showEmpleados.objects.raw(queryEmpleados, [EmpleadoID])
        for emp in empleados:
            empleado = emp

        fileName =  "Acuerdo de inventario recibido " + empleado.Nombre + " " + empleado.Apellido + "-" + inventario.CodigoInventario + " (" + fecha + ").pdf"

        response = HttpResponse(content_type='application/pdf') 
        response['Content-Disposition'] = 'filename="' + fileName + '"'

        pdf = SimpleDocTemplate(
            response,
            pagesize=letter,
            rightMargin=1.3* cm, leftMargin=1.3* cm, topMargin=0.5 * cm, bottomMargin=1.5 * cm
        )

        pdf.title = "Acuerdo de inventario recibido " + empleado.Nombre + " " + empleado.Apellido + "-" + inventario.CodigoInventario + " (" + fecha + ")"
        pdf.creator = "PoMoMin"
        pdf.author = "PoMoMin"
        
        titulo = Paragraph("Acuerdo de inventario recibido", stylesParraf['Title_RIGHT'])
        usuario = Paragraph("<b>Reporte solicitado por usuario:</b> " + str(request.session.get('Usuario', '')), stylesParraf['Normal'])
        fechaBloque = Paragraph("<b>Fecha y hora:</b> " + fecha, stylesParraf['Normal_RIGHT'])

        parrafo1 = Paragraph("Yo <b>" + empleado.Nombre + " " + empleado.Apellido + "</b> (" + empleado.Identificacion + ") al firmar este acuerdo, manifiesto que he recibido el inventario:", 
                        stylesParraf['Normal_JUSTIFY'])

        
        if inventario.TipoInventarioID == 1:
            data = [['Código Alfanumérico','Tipo Inventario','Categoría','Modelo','Serie','Sucursal']]
            lista = [str(inventario.CodigoInventario),'Equipo',str(inventario.Categoria),str(inventario.Modelo),str(inventario.Serie),str(inventario.Sucursal)]
            data.append(lista)
        else:
            data = [['Código Alfanumérico','Tipo Inventario','Categoría','Fabricante','Sucursal']]
            lista = [str(inventario.CodigoInventario),'Mobiliario',str(inventario.Categoria),str(inventario.Fabricante),str(inventario.Sucursal)]
            data.append(lista)
        table = Table(data, colWidths=[4*cm, 3*cm, 2*cm, 3.3*cm, 3.3*cm, 3*cm], repeatRows=1)
        table.setStyle(style)

        descripcion = Paragraph("<b>Descripción del inventario:</b>", 
                        stylesParraf['Normal_JUSTIFY'])
        if inventario.Descripcion is None or inventario.Descripcion == '':
            descripcion2 = Paragraph('No hay una descripción de las características físicas de el inventario entregado.', 
                        stylesParraf['Normal_JUSTIFY'])
            inventario.Descripcion = 'No hay una descripción de las características físicas de el inventario entregado.'
        else:
            descripcion2 = Paragraph(inventario.Descripcion, 
                            stylesParraf['Normal_JUSTIFY'])
            
        parrafo2 = Paragraph("En la fecha <b>" + str(asignacion.FechaVigente.strftime('%d-%m-%Y %H:%M')) + '</b> por motivo de <b>' + asignacion.MotivoAsignacion + '</b> estando el inventario en <b>Buen Estado</b>, tomando en cuenta, si las hay, las siguientes observaciones del inventario recibido.', 
                        stylesParraf['Normal_JUSTIFY'])

        notas = Paragraph("<b>Observaciones:</b>", 
                        stylesParraf['Normal_JUSTIFY'])
        lineas = Paragraph("______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________", 
                        stylesParraf['Normal_JUSTIFY'])

        dataHeader = [
            [my_image, titulo],
            [usuario, fechaBloque],
        ]
        
        tablaHeader = Table(dataHeader, [9.5 * cm, 9.5 * cm])
        tablaHeader.setStyle(styleHeader)

        dataFooter = [
            ['_________________________________________', '_________________________________________'],
            ['Soporte Técnico de TI', empleado.NombreCompleto]
        ]

        tablaFooter = Table(dataFooter, [9.5 * cm, 9.5 * cm])
        tablaFooter.setStyle(styleFirmas)

        elements = []
        elements.append(tablaHeader)
        elements.append(Spacer(1 * cm, 1 * cm))
        elements.append(parrafo1)
        elements.append(Spacer(0.5 * cm, 0.5 * cm))
        elements.append(table)
        elements.append(Spacer(1.5 * cm, 1.5 * cm))
        elements.append(descripcion)
        elements.append(descripcion2)
        elements.append(Spacer(1 * cm, 1 * cm))
        elements.append(parrafo2)
        elements.append(Spacer(1 * cm, 1 * cm))
        elements.append(notas)
        elements.append(lineas)

        if len(str(inventario.Descripcion)) <= 75:
            elements.append(Spacer(4 * cm, 4 * cm))
        else:
            elements.append(Spacer(3 * cm, 3 * cm))
        
        elements.append(tablaFooter)

        pdf.build(elements)

        return response
