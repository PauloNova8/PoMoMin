from django.shortcuts import render
from .models import *
from django.db import connection
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from dateutil import parser
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode


# EQUIPO
def equipo_insert_view(request, *args, **kwargs):
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
                params = (  request.POST['CodigoInventario'], request.POST['CodigoBarra'], int(request.POST['TipoInventarioID']),
                            int(request.POST['CategoriaID']), int(request.POST['FabricanteID']), request.POST['Modelo'], request.POST['Serie'], 
                            descripcion, int(request.POST['SucursalID']), int(request.POST['ProveedorID']), int(request.POST['EstadoID']), 
                            request.POST['FechaCompra'], None, fechaSoporte, 
                            notas, request.user.username, request.META.get('COMPUTERNAME'))
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
    
def equipo_buscar_view(request, *args, **kwargs):
    queryInventario = """SELECT * FROM v_Inventario WHERE TipoInventarioID = 1"""
    inventario = showInventario.objects.raw(queryInventario)
    context = {
        "showInventario": inventario,
        "device": request.META.get('COMPUTERNAME', '')
    }
    
    return render(request, 'buscarEquipo.html', context)

def equipo_actualizar_view(request, id):
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

    context = {
        "showCategorias": categorias,
        "showFabricantes": fabricantes,
        "showEstados": estados,
        "showSucursales": sucursales,
        "showProveedores": proveedores,
        "inventarioTraido": inventario,
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
                params = (  int(request.POST['InventarioID']), request.POST['CodigoInventario'],
                            int(request.POST['CategoriaID']), int(request.POST['FabricanteID']), request.POST['Modelo'], request.POST['Serie'], 
                            descripcion, int(request.POST['SucursalID']), int(request.POST['ProveedorID']), int(request.POST['EstadoID']), 
                            request.POST['FechaCompra'], None, fechaSoporte, 
                            notas, request.user.username, request.META.get('COMPUTERNAME'))
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
                params = (  int(request.POST['InventarioID']), 2, request.user.username, request.META.get('COMPUTERNAME'))
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

def escaner_view(request):
    
    context = {
        
    }
    
    return render(request, 'escaner.html', context)


# MOBILIARIO
def mobiliario_insert_view(request, *args, **kwargs):
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
                params = (  request.POST['CodigoInventario'], request.POST['CodigoBarra'], int(request.POST['TipoInventarioID']),
                            int(request.POST['CategoriaID']), int(request.POST['FabricanteID']), None, None, 
                            descripcion, int(request.POST['SucursalID']), int(request.POST['ProveedorID']), int(request.POST['EstadoID']), 
                            request.POST['FechaCompra'], fechaUtil, None, 
                            notas, request.user.username, request.META.get('COMPUTERNAME'))
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
    
def mobiliario_buscar_view(request, *args, **kwargs):
    queryInventario = """SELECT * FROM v_Inventario WHERE TipoInventarioID = 2"""
    inventario = showInventario.objects.raw(queryInventario)
    context = {
        "showInventario": inventario,
        "device": request.META.get('COMPUTERNAME', '')
    }
    
    return render(request, 'buscarMobiliario.html', context)

def mobiliario_actualizar_view(request, id):
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

    context = {
        "showCategorias": categorias,
        "showFabricantes": fabricantes,
        "showEstados": estados,
        "showSucursales": sucursales,
        "showProveedores": proveedores,
        "inventarioTraido": inventario,
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
                params = (  int(request.POST['InventarioID']), request.POST['CodigoInventario'],
                            int(request.POST['CategoriaID']), int(request.POST['FabricanteID']), None, None, 
                            descripcion, int(request.POST['SucursalID']), int(request.POST['ProveedorID']), int(request.POST['EstadoID']), 
                            request.POST['FechaCompra'], fechaUtil, None, 
                            notas, request.user.username, request.META.get('COMPUTERNAME'))
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
                params = (  int(request.POST['InventarioID']), 2, request.user.username, request.META.get('COMPUTERNAME'))
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
