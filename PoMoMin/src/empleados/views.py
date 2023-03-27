from django.shortcuts import redirect, render
from .models import *
from usuarios.models import showUsuarios
from usuarios.views import login_view
from inventario.views import home_view
from inventario.models import showSucursales
from django.db import connection
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from dateutil import parser
from django.views.decorators.cache import cache_control

# EMPLEADOS
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def empleado_insert_view(request, *args, **kwargs):
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
        if request.session.get('PerfilID', '') != 1: 
            return redirect(home_view)
        
        querySucursales = "SELECT 1 AS id, SucursalID, Nombre FROM Sucursales WHERE Activo = 1"
        sucursales = showSucursales.objects.raw(querySucursales)

        queryDepartamentos = "SELECT 1 AS id, DepartamentoID, Nombre FROM Departamentos"
        departamentos = showDepartamentos.objects.raw(queryDepartamentos)

        queryEstados = "SELECT 1 AS id, EstadoID, Estado FROM EstadosEmpleado"
        estados = showEstados.objects.raw(queryEstados)

        context = {
            "showDepartamentos": departamentos,
            "showEstados": estados,
            "showSucursales": sucursales,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'insertarEmpleado.html', context)

def cargar_puestos(request):
    if request.method == 'POST':
        idPuestoEmpleado = request.POST.get('PuestoID', '')
        try:
            with connection.cursor() as cursor:
                query ='''SET NOCOUNT ON;
                                    SELECT PuestoID, Nombre FROM Puestos WHERE DepartamentoID = %s'''
                params = (  request.POST['DepartamentoID'] )
                cursor.execute(query, params)
                puestos = cursor.fetchall()
                
                if idPuestoEmpleado == '':
                    response = "<option value=''>Seleccione una opción</option>"
                    for row in puestos:
                        response += "<option value='" + str(row[0]) + "'>" + str(row[1]) + "</option>"
                else:
                    response = "<option value=''>Seleccione una opción</option>"
                    for row in puestos:
                        if str(row[0]) == str(idPuestoEmpleado):
                            response += "<option selected value='" + str(row[0]) + "'>" + str(row[1]) + "</option>"
                        else:
                            response += "<option value='" + str(row[0]) + "'>" + str(row[1]) + "</option>"
                
                return HttpResponse(response)
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()

def cargar_jefes(request):
    if request.method == 'POST':
        idReportaAEmpleado = request.POST.get('ReportaAEmpleado', '')
        try:
            with connection.cursor() as cursor:
                query ='''SET NOCOUNT ON;
                          SELECT E.EmpleadoID, CASE WHEN CHARINDEX(' ', E.Nombres) = 0 
								   THEN E.Nombres 
								   ELSE LEFT(E.Nombres + ' ', CHARINDEX(' ', E.Nombres) - 1) END AS Nombre,
							  CASE WHEN CHARINDEX(' ', E.Apellidos) = 0 
								   THEN E.Apellidos 
								   ELSE LEFT(E.Apellidos + ' ', CHARINDEX(' ', E.Apellidos) - 1) END AS Apellido,
				              P.Nombre AS PuestoTexto 
                          FROM Empleados AS E INNER JOIN Puestos AS P ON E.PuestoID = P.PuestoID
                          WHERE E.EstadoID = 1 AND P.DepartamentoID = %s AND SucursalID = %s AND P.PuestoID IN(1,2,5,6,7,8,10,14,15,19,22,28,29,30,31,32,33,34)'''
                params = (  request.POST['DepartamentoID'], request.POST['SucursalID'] )
                cursor.execute(query, params)
                jefes = cursor.fetchall()
                
                if idReportaAEmpleado == '':
                    response = "<option value=''>Seleccione una opción</option><option value='Ninguno'>Ninguno</option>"
                    for row in jefes:
                        response += "<option value='" + str(row[0]) + "'>" + str(row[1]) + " "  + str(row[2]) + " | " + str(row[3]) + "</option>"
                else:
                    if idReportaAEmpleado == 'None':
                        response = "<option value=''>Seleccione una opción</option><option selected value='Ninguno'>Ninguno</option>"
                    else:
                        response = "<option value=''>Seleccione una opción</option><option value='Ninguno'>Ninguno</option>"
                        for row in jefes:
                            if str(row[0]) == str(idReportaAEmpleado):
                                response += "<option selected value='" + str(row[0]) + "'>" + str(row[1]) + " "  + str(row[2]) + " | " + str(row[3]) + "</option>"
                            else:
                                response += "<option value='" + str(row[0]) + "'>" + str(row[1]) + " "  + str(row[2]) + " | " + str(row[3]) + "</option>"
                
                return HttpResponse(response)
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()

def sp_insertar_empleado(request):
    if request.method == 'POST':
        try:
            conteo = 0
            reportaA = request.POST['ReportaA']
            fechaBaja = request.POST['FechaBaja']
            numCel = request.POST['TelefonoCelular']
            numTrabajo = request.POST['TelefonoTrabajo']
            direccion = request.POST['Direccion']
            notas = request.POST['Notas']
            if(request.POST['ReportaA'] == 'Ninguno'):
                reportaA = None
            if(request.POST['FechaBaja'] == ''):
                 fechaBaja = None
            if(request.POST['TelefonoCelular'] == ''):
                 numCel = None
            if(request.POST['TelefonoTrabajo'] == ''):
                 numTrabajo = None
            if(request.POST['Direccion'] == ''):
                 direccion = None
            if(request.POST['Notas'] == ''):
                 notas = None
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @ID AS INT;
                                    EXEC INSERT_EMPLEADO %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, @ID = @ID OUTPUT
                                    SELECT @ID AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  request.POST['Nombres'], request.POST['Apellidos'], request.POST['Identificacion'],
                            int(request.POST['SucursalID']), int(request.POST['PuestoID']), reportaA, numCel, 
                            numTrabajo, direccion, request.POST['Genero'], request.POST['FechaNacimiento'], 
                            request.POST['FechaAlta'], fechaBaja, int(request.POST['EstadoID']), 
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
def empleado_buscar_view(request, *args, **kwargs):
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
        if request.session.get('PerfilID', '') != 1: 
            return redirect(home_view)
        
        queryInventario = """SELECT * FROM v_Empleados"""
        empleado = showEmpleados.objects.raw(queryInventario)
        context = {
            "showEmpleados": empleado,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'buscarEmpleado.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def empleado_actualizar_view(request, id):
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
        if request.session.get('PerfilID', '') != 1: 
            return redirect(home_view)
        
        queryEmpleados = """SELECT * FROM v_Empleados WHERE EmpleadoID = %s"""
        empleados = showEmpleados.objects.raw(queryEmpleados, [int(id)])

        querySucursales = "SELECT 1 AS id, SucursalID, Nombre, Activo FROM Sucursales ORDER BY Activo DESC" 
        sucursales = showSucursales.objects.raw(querySucursales)

        queryDepartamentos = "SELECT 1 AS id, DepartamentoID, Nombre FROM Departamentos"
        departamentos = showDepartamentos.objects.raw(queryDepartamentos)

        queryEstados = "SELECT 1 AS id, EstadoID, Estado FROM EstadosEmpleado"
        estados = showEstados.objects.raw(queryEstados)

        for obj in empleados:
            empleado = obj
        
        obj.FechaNacimiento = parser.parse(str(obj.FechaNacimiento))
        obj.FechaAlta = parser.parse(str(obj.FechaAlta))
        if(obj.FechaBaja != None):
            obj.FechaBaja = parser.parse(str(obj.FechaBaja))
        
        if(obj.Direccion == None):
            obj.Direccion = ""

        if(obj.Notas == None):
            obj.Notas = ""

        context = {
            "showDepartamentos": departamentos,
            "showEstados": estados,
            "showSucursales": sucursales,
            "device": request.META.get('COMPUTERNAME', ''),
            "empleadoTraido" : empleado
        }
        
        return render(request, 'actualizarEmpleado.html', context)

def sp_actualizar_empleado(request):
    if request.method == 'POST':
        try:
            conteo = 0
            reportaA = request.POST['ReportaA']
            fechaBaja = request.POST['FechaBaja']
            numCel = request.POST['TelefonoCelular']
            numTrabajo = request.POST['TelefonoTrabajo']
            direccion = request.POST['Direccion']
            notas = request.POST['Notas']
            if(request.POST['ReportaA'] == 'Ninguno'):
                reportaA = None
            if(request.POST['FechaBaja'] == ''):
                 fechaBaja = None
            if(request.POST['TelefonoCelular'] == ''):
                 numCel = None
            if(request.POST['TelefonoTrabajo'] == ''):
                 numTrabajo = None
            if(request.POST['Direccion'] == ''):
                 direccion = None
            if(request.POST['Notas'] == ''):
                 notas = None
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC UPDATE_EMPLEADO %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['EmpleadoID']), request.POST['Nombres'], request.POST['Apellidos'], request.POST['Identificacion'],
                            int(request.POST['SucursalID']), int(request.POST['PuestoID']), reportaA, numCel, 
                            numTrabajo, direccion, request.POST['Genero'], request.POST['FechaNacimiento'], 
                            request.POST['FechaAlta'], fechaBaja, int(request.POST['EstadoID']), 
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
    
def sp_desactivar_empleado(request):
    if request.method == 'POST':
        try:
            conteo = 0
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC DEACTIVATE_EMPLEADO %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['EmpleadoID']), 2, 
                            request.session.get('Usuario', ''), device)
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

