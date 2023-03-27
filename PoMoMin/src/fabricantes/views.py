from django.shortcuts import redirect, render
from .models import *
from usuarios.models import showUsuarios
from usuarios.views import login_view
from inventario.views import home_view
from django.db import connection
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from inventario.models import showFabricantes
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fabricante_insert_view(request, *args, **kwargs):
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
        
        context = {
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'insertarFabricante.html', context)

def sp_insertar_fabricante(request):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @ID AS INT;
                                    EXEC INSERT_FABRICANTE %s, %s, %s, %s, @ID = @ID OUTPUT
                                    SELECT @ID AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  request.POST['Nombre'], request.POST['Descripcion'],
                            request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':1, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':0, 'Mensaje': 'Ha devuelto un error.'})
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
def fabricante_buscar_view(request, *args, **kwargs):
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
        
        queryFabricantes = """SELECT * FROM v_Fabricantes"""
        fabricantes = showFabricantes.objects.raw(queryFabricantes)
        context = {
            "showFabricantes": fabricantes,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'buscarFabricante.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fabricante_actualizar_view(request, id):
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
        
        queryFabricante = """SELECT * FROM v_Fabricantes WHERE FabricanteID = %s"""
        fabricantes = showFabricantes.objects.raw(queryFabricante, [int(id)])

        for obj in fabricantes:
            fabricante = obj
        
        if(obj.Descripcion == None):
            obj.Descripcion = ""

        context = {
            "fabricanteTraido": fabricante,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'actualizarFabricante.html', context)

def sp_actualizar_fabricante(request):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC UPDATE_FABRICANTE %s, %s, %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['FabricanteID']), request.POST['Nombre'],
                            request.POST['Descripcion'], int(request.POST['Activo']),
                            request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':1, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':0, 'Mensaje': 'Ha devuelto un error.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
    
def sp_desactivar_fabricante(request):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                storedProcedure ='''SET NOCOUNT ON;
                                    DECLARE @RESULT AS INT;
                                    EXEC UPDATE_FABRICANTE %s, %s, %s, %s, %s, %s, @RESULT = @RESULT OUTPUT
                                    SELECT @RESULT AS REPUESTA'''
                if request.user_agent.device.family == 'Other':
                    device = 'PC' + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                else:
                    device = request.user_agent.device.family + " " + request.user_agent.os.family + " " + request.user_agent.os.version_string
                params = (  int(request.POST['FabricanteID']), None, None, 0, 
                            request.session.get('Usuario', ''), device)
                cursor.execute(storedProcedure, params)
                respuesta = int(cursor.fetchone()[0])

                if respuesta == 1:
                    response = JsonResponse({'Estado':1, 'Mensaje': 'Insertado correctamente.'})
                    response.status_code = 200 #Ok
                    return response
                else:
                    response = JsonResponse({'Estado':0, 'Mensaje': 'Ha devuelto un error.'})
                    response.status_code = 400 #Bad Request
                    return response
        except Exception as err:
                response = JsonResponse({'Estado':-2, 'Mensaje': 'Ocurrio un error al enviar la solicitud.'})
                print(err)
                response.status_code = 500 #Internal Error
                return response
    else:
        return HttpResponseForbidden()
