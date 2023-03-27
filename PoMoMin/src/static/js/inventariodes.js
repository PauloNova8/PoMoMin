$(document).ready(function(){
    $('#TablaEquipoDes').DataTable( {
        "pageLength" : 10,
        "ordering": false,
        "bPaginate": false,
        "language": {
            processing: "Procesando...",
            search: "Buscar inventario por código",
            lengthMenu: "",
            info: "",
            infoEmpty: "",
            infoFiltered: "",
            infoPostFix: "",
            loadingRecords: "Cargando filas...",
            zeroRecords: "Filtre con el código del inventario para mostrar",
            emptyTable: "Filtre con el código del inventario para mostrar",
            aria: {
                sortAscending:  ": activar para ordenar la columna en orden ascendente",
                sortDescending: ": activar para ordenar la columna en orden descendente"
            }
        }
    } );
    
    document.getElementById("TablaEquipoDes_filter").
    querySelector('label').
    querySelector('input').id = "barraBusquedaDes";
});

function detectCheckBoxDes(){
    if (document.getElementById('inventarioSeleccionado').checked) {
        var valor = document.getElementById('inventarioSeleccionado').value;
        document.getElementById('InventarioID').value = valor;
        document.getElementById('EmpleadoID').value = document.getElementById("AsignadoAID").value;

    } else {
        document.getElementById('InventarioID').value = '';
        document.getElementById('EmpleadoID').value = '';
    }
}

$(document).ready(function(){
    $('#barraBusquedaDes').keyup(function(){
        var searchStr = $(this).val();
        filterDataDes();
        document.getElementById('InventarioID').value = '';
        document.getElementById('EmpleadoID').value = '';
    });
});

function filterDataDes(){
if ($('#barraBusquedaDes').length){
    barraBusqueda = document.getElementById("barraBusquedaDes").value;
} else {
    barraBusqueda = '';
}
if(document.getElementById("barraBusquedaDes").value != ''){
    $.ajax({
        type: "POST",
        url: "cargarInventario/",
        data: {
            "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
            "codigo" : document.getElementById('barraBusquedaDes').value
        },
        success: function (respuesta) {
            if(respuesta != ''){
                $('#cuerpoTablaDes').html(respuesta);
                EmpleadoTraidoID = document.getElementById("AsignadoAID").value;
                document.getElementById("EmpleadoID").value = EmpleadoTraidoID;
                filterDataEDes(EmpleadoTraidoID);
                cargarFecha();

            } else {
                $('#cuerpoTablaDes').html('<tr class="odd"><td valign="top" colspan="7" class="dataTables_empty">El código filtrado no fue encontrado o no está asignado a ningún empleado</td></tr>');
                document.getElementById('EmpleadoID').value = '';
            }
        }
    });
    return false;
}
}

$(document).ready(function(){
    $('#TablaEmpleadosDes').DataTable( {
        "pageLength" : 10,
        "ordering": false,
        "bPaginate": false,
        "language": {
            processing: "Procesando...",
            search: "Buscar empleado por identidad",
            lengthMenu: "",
            info: "",
            infoEmpty: "",
            infoFiltered: "",
            infoPostFix: "",
            loadingRecords: "Cargando filas...",
            zeroRecords: "Se mostrará el empleado al que esté asignado el inventario",
            emptyTable: "Se mostrará el empleado al que esté asignado el inventario",
            aria: {
                sortAscending:  ": activar para ordenar la columna en orden ascendente",
                sortDescending: ": activar para ordenar la columna en orden descendente"
            }
        }
    } );
    
    document.getElementById("TablaEmpleadosDes_filter").
    querySelector('label').
    querySelector('input').id = "barraBusquedaEDes";
});

function filterDataEDes(id){
if (document.getElementById("EmpleadoID").length){
    barraBusqueda = document.getElementById("EmpleadoID").value;
} else {
    barraBusqueda = '';
    $('#cuerpoTablaEDes').html('<tr class="odd"><td valign="top" colspan="7" class="dataTables_empty">Se mostrará el empleado al que esté asignado el inventario</td></tr>');
}
if(document.getElementById("EmpleadoID").value != ''){
    $.ajax({
        type: "POST",
        url: "cargarEmpleado/",
        data: {
            "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
            "EmpleadoID" : document.getElementById("EmpleadoID").value
        },
        success: function (respuesta) {
            if(respuesta != ''){
                $('#cuerpoTablaEDes').html(respuesta);
            } else {
                $('#cuerpoTablaEDes').html('<tr class="odd"><td valign="top" colspan="7" class="dataTables_empty">No se ha encontrado el empleado</td></tr>');
            }
        }
    });
    return false;
}
}

function cargarFecha(){
    if (document.getElementById("EmpleadoID").length && document.getElementById("InventarioID").length){
        EmpleadoID = document.getElementById("EmpleadoID").value;
        InventarioID = document.getElementById("EmpleadoID").value;
    } else {
        EmpleadoID = '';
        InventarioID = '';
    }
    if(document.getElementById("EmpleadoID").value != '' && document.getElementById('inventarioSeleccionado').value != ''){
        $.ajax({
            type: "POST",
            url: "cargarFecha/",
            data: {
                "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                "EmpleadoID" : document.getElementById("EmpleadoID").value,
                "InventarioID" : document.getElementById("inventarioSeleccionado").value
            },
            success: function (respuesta) {
                if(respuesta != ''){
                    document.getElementById("FechaAsignacion").value = respuesta
                }
            }
        });
        return false;
    }
}


function showSuccessMessage(mensaje) { 
    toastr.success(mensaje
                    ,"¡Exito!"
                    ,{positionClass:"toast-bottom-right"
                    ,timeOut:8e3
                    ,closeButton:!0
                    ,debug:!1
                    ,newestOnTop:!0
                    ,progressBar:!0
                    ,preventDuplicates:!0
                    ,onclick:null
                    ,showDuration:"300"
                    ,hideDuration:"3000"
                    ,extendedTimeOut:"3000"
                    ,showEasing:"swing"
                    ,hideEasing:"linear"
                    ,showMethod:"fadeIn"
                    ,hideMethod:"fadeOut"
                    ,tapToDismiss:!1}
                );
}

function showErrorMessage(mensaje) { 
    toastr.error(mensaje
                    ,'¡Error!'
                    ,{positionClass:"toast-bottom-right"
                    ,timeOut:8e3
                    ,closeButton:!0
                    ,debug:!1
                    ,newestOnTop:!0
                    ,progressBar:!0
                    ,preventDuplicates:!0
                    ,onclick:null
                    ,showDuration:"300"
                    ,hideDuration:"3000"
                    ,extendedTimeOut:"3000"
                    ,showEasing:"swing"
                    ,hideEasing:"linear"
                    ,showMethod:"fadeIn"
                    ,hideMethod:"fadeOut"
                    ,tapToDismiss:!1}
                );
}

function validar(){
    if (document.getElementById("InventarioID").value.length != 0) { 
        if (document.getElementById("InventarioID").value == "") {
            showErrorMessage('Debe seleccionar el checkbox del inventario para desasignarlo.');
            return false
        }
    } else {
        showErrorMessage('Debe seleccionar el checkbox del inventario para desasignarlo.');
        return false
    }
    if (document.getElementById("EmpleadoID").value.length != 0) { 
        if (document.getElementById("EmpleadoID").value == "") {
            showErrorMessage('Debe seleccionar a un empleado para la desasignación.');
            return false
        }
    } else {
        showErrorMessage('Debe seleccionar a un empleado para la desasignación.');
        return false
    }
    if(document.getElementById("MotivoID").value == ""){
        showErrorMessage('Debe seleccionar un motivo para la desasignación.');
        return false
    }
    return true;
}

function desasignarInventario(){
    if(validar()){
        $.ajax({
            type: 'POST',
            url: 'desasignar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    InventarioID : document.getElementById("InventarioID").value,
                    EmpleadoID : document.getElementById("EmpleadoID").value,
                    MotivoID : document.getElementById("MotivoID").value,
                    Notas : document.getElementById("Notas").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('Se desasignó el inventario correctamente.');
                limpiar();
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se pudo desasignar el inventario, se presentó un error interno.');
            }
        });
    }
}

function limpiar(){
    document.getElementById("barraBusquedaDes").value = ""
    $('#barraBusquedaDes').keyup();
    filterDataEDes('')
    document.getElementById("FechaAsignacion").value = ""
    document.getElementById("InventarioID").value = ""
    document.getElementById("EmpleadoID").value = ""
    document.getElementById("MotivoID").value = ""
    document.getElementById("Notas").value = ""
}
