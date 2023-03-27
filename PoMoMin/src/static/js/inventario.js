$(document).ready(function(){
    $('#TablaEquipo').DataTable( {
        "pageLength" : 10,
        "ordering": false,
        "bPaginate": false,
        "aaSorting": [],
            columnDefs: [{
            orderable: false,
            targets: 6
            }],
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
    
    document.getElementById("TablaEquipo_filter").
    querySelector('label').
    querySelector('input').id = "barraBusqueda";
});

function detectCheckBox(){
    if (document.getElementById('inventarioSeleccionado').checked) {
        var valor = document.getElementById('inventarioSeleccionado').value;
        document.getElementById('InventarioID').value = valor;
    } else {
        document.getElementById('InventarioID').value = '';
    }
}

$(document).ready(function(){
    $('#barraBusqueda').keyup(function(){
        var searchStr = $(this).val();
        filterData();
        document.getElementById('InventarioID').value = '';
    });
});

function filterData(){
if ($('#barraBusqueda').length){
    barraBusqueda = document.getElementById("barraBusqueda").value;
} else {
    barraBusqueda = '';
}
if(document.getElementById("barraBusqueda").value != ''){
    $.ajax({
        type: "POST",
        url: "cargarInventario/",
        data: {
            "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
            "codigo" : document.getElementById('barraBusqueda').value
        },
        success: function (respuesta) {
            if(respuesta != ''){
                $('#cuerpoTabla').html(respuesta);
            } else {
                $('#cuerpoTabla').html('<tr class="odd"><td valign="top" colspan="7" class="dataTables_empty">El código filtrado no fue encontrado o el invantario ya está asignado a un empleado</td></tr>');
            }
        }
    });
    return false;
}
}

$(document).ready(function(){
    $('#TablaEmpleados').DataTable( {
        "pageLength" : 10,
        "ordering": false,
        "bPaginate": false,
        "aaSorting": [],
            columnDefs: [{
            orderable: false,
            targets: 6
            }],
        "language": {
            processing: "Procesando...",
            search: "Buscar empleado por identidad",
            lengthMenu: "",
            info: "",
            infoEmpty: "",
            infoFiltered: "",
            infoPostFix: "",
            loadingRecords: "Cargando filas...",
            zeroRecords: "Filtre con el número de identidad del empleado para mostrar",
            emptyTable: "Filtre con el número de identidad del empleado para mostrar",
            aria: {
                sortAscending:  ": activar para ordenar la columna en orden ascendente",
                sortDescending: ": activar para ordenar la columna en orden descendente"
            }
        }
    } );
    
    document.getElementById("TablaEmpleados_filter").
    querySelector('label').
    querySelector('input').id = "barraBusquedaE";

    var barraBusquedaE = document.getElementById('barraBusquedaE');
    barraBusquedaE.setAttribute("type", "text");
    barraBusquedaE.setAttribute("data-placeholder", "____-____-_____");
    barraBusquedaE.setAttribute("data-slots", "_");

    mascara();
});

//CREACION DE MASCARAS PARA LOS INPUTS
function mascara(){
    for (const el of document.querySelectorAll("[data-placeholder][data-slots]")) {
        const pattern = el.getAttribute("data-placeholder"),
            slots = new Set(el.dataset.slots || "_"),
            prev = (j => Array.from(pattern, (c,i) => slots.has(c)? j=i+1: j))(0),
            first = [...pattern].findIndex(c => slots.has(c)),
            accept = new RegExp(el.dataset.accept || "\\d", "g"),
            clean = input => {
                input = input.match(accept) || [];
                return Array.from(pattern, c =>
                    input[0] === c || slots.has(c) ? input.shift() || c : c
                );
            },
            format = () => {
                const [i, j] = [el.selectionStart, el.selectionEnd].map(i => {
                    i = clean(el.value.slice(0, i)).findIndex(c => slots.has(c));
                    return i<0? prev[prev.length-1]: back? prev[i-1] || first: i;
                });
                el.value = clean(el.value).join``;
                el.setSelectionRange(i, j);
                back = false;
            };
        let back = false;
        el.addEventListener("keydown", (e) => back = e.key === "Backspace");
        el.addEventListener("input", format);
        el.addEventListener("focus", format);
        el.addEventListener("blur", () => el.value === pattern && (el.value=""));
    }
}

function detectCheckBoxE(){
    if (document.getElementById('empleadoSeleccionado').checked) {
        var valor = document.getElementById('empleadoSeleccionado').value;
        document.getElementById('EmpleadoID').value = valor;
    } else {
        document.getElementById('EmpleadoID').value = '';
    }
}

$(document).ready(function(){
    $('#barraBusquedaE').keyup(function(){
        var searchStr = $(this).val();
        filterDataE();
        document.getElementById('EmpleadoID').value = '';
    });
});

function filterDataE(){
if ($('#barraBusquedaE').length){
    barraBusqueda = document.getElementById("barraBusquedaE").value;
} else {
    barraBusqueda = '';
}
if(document.getElementById("barraBusquedaE").value != ''){
    $.ajax({
        type: "POST",
        url: "cargarEmpleado/",
        data: {
            "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
            "identidad" : document.getElementById('barraBusquedaE').value
        },
        success: function (respuesta) {
            if(respuesta != ''){
                $('#cuerpoTablaE').html(respuesta);
            } else {
                $('#cuerpoTablaE').html('<tr class="odd"><td valign="top" colspan="7" class="dataTables_empty">Filtre con el número de identidad del empleado para mostrar</td></tr>');
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
            showErrorMessage('Debe seleccionar un inventario para asignarlo.');
            return false
        }
    } else {
        showErrorMessage('Debe seleccionar un inventario para asignarlo.');
        return false
    }
    if (document.getElementById("EmpleadoID").value.length != 0) { 
        if (document.getElementById("EmpleadoID").value == "") {
            showErrorMessage('Debe seleccionar a un empleado para la asignación.');
            return false
        }
    } else {
        showErrorMessage('Debe seleccionar a un empleado para la asignación.');
        return false
    }
    if(document.getElementById("MotivoID").value == ""){
        showErrorMessage('Debe seleccionar un motivo para la asignación.');
        return false
    }
    return true;
}

function asignarInventario(){
    if(validar()){
        $.ajax({
            type: 'POST',
            url: 'asignar/',
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
                showSuccessMessage('Se asignó el inventario correctamente. Será redireccionado al acuerdo de recibido en PDF.');
                setTimeout(function () {
                    document.getElementById("mostrarReporte").click();
                }, 1000);
                limpiar();
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se pudo asignar el inventario, se presentó un error interno.');
            }
        });
    }
}

function limpiar(){
    document.getElementById("barraBusqueda").value = ""
    $('#barraBusqueda').keyup();
    document.getElementById("barraBusquedaE").value = ""
    $('#barraBusquedaE').keyup();
    document.getElementById("InventarioID").value = ""
    document.getElementById("EmpleadoID").value = ""
    document.getElementById("MotivoID").value = ""
    document.getElementById("Notas").value = ""
}