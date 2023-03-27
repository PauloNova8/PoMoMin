from django.shortcuts import redirect, render
from .models import *
from usuarios.models import showUsuarios
from usuarios.views import login_view
from inventario.views import home_view
from django.db import connection
from dateutil import parser
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bitacora_buscar_view(request, *args, **kwargs):
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
        
        queryBitacora = """SELECT 1 AS id, * FROM Bitacora ORDER BY NoRegistro DESC"""
        bitacora = showBitacora.objects.raw(queryBitacora)
        context = {
            "showBitacora": bitacora,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'buscarBitacora.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bitacora_detalles_view(request, id):
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
        
        queryBitacora = """SELECT 1 AS id, * FROM Bitacora WHERE NoRegistro = %s"""
        bitacora = showBitacora.objects.raw(queryBitacora, [int(id)])

        for obj in bitacora:
            registro = obj
        
        obj.FechaHoraEvento = parser.parse(str(obj.FechaHoraEvento))

        context = {
            "registroTraido": registro,
            "device": request.META.get('COMPUTERNAME', '')
        }
        
        return render(request, 'verRegistro.html', context)
