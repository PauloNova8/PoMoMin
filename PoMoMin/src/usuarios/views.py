from django.shortcuts import render
from .models import *
from django.db import connection
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from dateutil import parser
from django.shortcuts import redirect
from django.views.decorators.cache import cache_control


# USUARIO
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def usuario_insert_view(request, *args, **kwargs):
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
            return redirect(usuario_actualizar_view, id=request.session.get('UsuarioID', 0))
        
        queryPerfiles = "SELECT 1 AS id, PerfilID, NombrePerfil FROM PerfilesUsuario"
        perfiles = showPerfiles.objects.raw(queryPerfiles)

        queryEstados = "SELECT 1 AS id, EstadoID, Estado FROM EstadosUsuario"
        estados = showEstados.objects.raw(queryEstados)

        context = {
            "showPerfiles": perfiles,
            "showEstados": estados,
            "device": request.META.get('COMPUTERNAME', '')
        }
            
        return render(request, 'insertarUsuario.html', context)

def sp_insertar_usuario(request):
    if request.method == 'POST':
        try:
            conteo = 0
            token = request.POST['Token']
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @ID AS INT;
                                    EXEC INSERT_USUARIO %s, %s, %s, %s, %s, %s, @ID = @ID OUTPUT
                                    SELECT @ID AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  request.POST['Usuario'], token, int(request.POST['PerfilID']),
                            int(request.POST['EstadoID']), request.session.get('Usuario', ''), device)
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
def usuario_buscar_view(request, *args, **kwargs):
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
            return redirect(usuario_actualizar_view, id=request.session.get('UsuarioID', 0))
        
        queryUsuarios = """SELECT * FROM v_Usuarios"""
        usuarios = showUsuarios.objects.raw(queryUsuarios)
        context = {
            "showUsuarios": usuarios,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'buscarUsuario.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def usuario_actualizar_view(request, id):
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
            id = request.session.get('UsuarioID', 0)
        
        queryUsuarios = """SELECT * FROM v_Usuarios WHERE UsuarioID = %s"""
        usuarios = showUsuarios.objects.raw(queryUsuarios, [int(id)])

        queryPerfiles = "SELECT 1 AS id, PerfilID, NombrePerfil FROM PerfilesUsuario"
        perfiles = showPerfiles.objects.raw(queryPerfiles)

        queryEstados = "SELECT 1 AS id, EstadoID, Estado FROM EstadosUsuario"
        estados = showEstados.objects.raw(queryEstados)

        for obj in usuarios:
            usuario = obj
        
        obj.FechaCreacion = parser.parse(str(obj.FechaCreacion))
        if(obj.FechaUltimaActualizacion != None):
            obj.FechaUltimaActualizacion = parser.parse(str(obj.FechaUltimaActualizacion))

        context = {
            "showPerfiles": perfiles,
            "showEstados": estados,
            "usuarioTraido": usuario,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'actualizarUsuario.html', context)

def sp_actualizar_usuario(request):
    if request.method == 'POST':
        try:
            conteo = 0
            clave = request.POST['Token']
            if(clave == ''):
                token = None
            else:
                token = request.POST['Token']

            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC UPDATE_USUARIO %s, %s, %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['UsuarioID']), token,
                            int(request.POST['PerfilID']), int(request.POST['EstadoID']), 
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
    
def sp_desactivar_usuario(request):
    if request.method == 'POST':
        try:
            conteo = 0
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC UPDATE_USUARIO %s, %s, %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['UsuarioID']), None,
                            None, 2, 
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request, *args, **kwargs):
    context = {
        "device": request.META.get('COMPUTERNAME', '')
    }
    
    return render(request, 'login.html', context)

def login(request):
    if request.method == 'POST':
        try:
            conteo = 0
            token = request.POST['Token']
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @ID AS INT;
                                    EXEC INICIO_SESION %s, %s, @ID = @ID OUTPUT
                                    SELECT @ID AS REPUESTA'''
                params = (  request.POST['Usuario'], token)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 0:
                    response = JsonResponse({'Estado':conteo, 'Mensaje': 'Ha devuelto un error.'})
                    response.status_code = 400 #Bad Request
                    return response
                else:
                    response = JsonResponse({'ID':respuesta, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
    
def kill_session(request):
    del request.session['UsuarioID']
    del request.session['Usuario']
    del request.session['PerfilID']
    del request.session['EstadoID']
    
    return redirect(login_view)