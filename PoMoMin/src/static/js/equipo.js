function insertarEquipo() {
    var form = document.getElementById('formulario');
    if (document.getElementById("FechaUltimoSoporte").value.length != 0) { 
        var d1 = new Date(document.getElementById("FechaCompra").value);
        var d2 = new Date(document.getElementById("FechaUltimoSoporte").value);
        if (d1.getTime() > d2.getTime()) {
            showErrorMessage('La fecha de soporte no puede ser antes de la fecha de compra.');
            return false
        }
    }
    if (document.getElementById("CodigoBarra").value == "sincodigo") {
        showErrorMessage('Debe generar un código QR o de barras para el equipo.');
    }else if(!form.checkValidity()) {
            form.querySelector('#validate').click();
    } else {
        $.ajax({
            type: 'POST',
            url: 'equipoInsertar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    CodigoInventario : document.getElementById("CodigoInventario").value,
                    CodigoBarra : document.getElementById("CodigoBarra").value,
                    TipoInventarioID : document.getElementById("TipoInventarioID").value,
                    CategoriaID : document.getElementById("CategoriaID").value,
                    FabricanteID : document.getElementById("FabricanteID").value,
                    Modelo : document.getElementById("Modelo").value,
                    Serie : document.getElementById("Serie").value,
                    Descripcion : document.getElementById("Descripcion").value,
                    SucursalID : document.getElementById("SucursalID").value,
                    ProveedorID : document.getElementById("ProveedorID").value,
                    EstadoID : document.getElementById("EstadoID").value,
                    FechaCompra : document.getElementById("FechaCompra").value,
                    FechaUltimoSoporte : document.getElementById("FechaUltimoSoporte").value,
                    Notas : document.getElementById("Notas").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('Se ha registrado el equipo exitosamente.');
                form.reset();
                cargarNoCodeImagen();
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se registró el equipo. Este código alfanumérico ya existe.');
            }
        });
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

$(document).ready(function(){
    $('#TablaEquipo').DataTable( {
        "pageLength" : 10,
        "order": [[ 0, "asc" ]],
        "aaSorting": [],
            columnDefs: [{
            orderable: false,
            targets: 6
            }],
        "language": {
            processing: "Procesando...",
            search: "Buscar",
            lengthMenu: "Mostrar _MENU_ filas",
            info: "Mostrando _START_ a _END_ de _TOTAL_ filas",
            infoEmpty: "Mostrando 0 a 0 de 0 filas",
            infoFiltered: "(filtrado de _MAX_ filas en total)",
            infoPostFix: "",
            loadingRecords: "Cargando filas...",
            zeroRecords: "No hay filas por mostrar",
            emptyTable: "No hay datos disponibles en la tabla",
            paginate: {
                first: "Primero",
                previous: "Anterior",
                next: "Siguiente",
                last: "Ultimo"
            },
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

function validaciones(){
    if (document.getElementById("FechaUltimoSoporte").value.length != 0) { 
        var d1 = new Date(document.getElementById("FechaCompra").value);
        var d2 = new Date(document.getElementById("FechaUltimoSoporte").value);
        if (d1.getTime() > d2.getTime()) {
            showErrorMessage('La fecha de soporte no puede ser antes de la fecha de compra.');
            return false
        }
    }

    let respuestaSweet = new Promise(
        function(myResolve, myReject) { 
            if (document.getElementById("EstadoID").value == 2) {
                swal({  
                    title: "¿Actualizar el equipo a 'Inactivo'?",  
                    text: "Al desactivarlo el equipo se desasignará de cualquier empleado al que esté asignado.",
                    showCancelButton: true,  
                    confirmButtonColor: '#dc3545', 
                    confirmButtonTextColor: 'white',  
                    confirmButtonText: "¡Desactivar!",  
                    cancelButtonText: "Cancelar",  
                    closeOnConfirm: true,  
                    closeOnCancel: true  
                },  
                function(isConfirm) {
                    if (isConfirm) {
                        myResolve(true);
                    } else {
                        myReject(false);
                    }
                }) 
            } else if (document.getElementById("EstadoID").value == 3) {
                swal({  
                    title: "¿Actualizar el equipo como 'En espera de soporte'?",  
                    text: "Al marcarlo de este modo el equipo se desasignará de cualquier empleado al que esté asignado.",
                    showCancelButton: true,  
                    confirmButtonColor: '#e7b63a', 
                    confirmButtonTextColor: 'white',  
                    confirmButtonText: "Continuar",  
                    cancelButtonText: "Cancelar", 
                    closeOnCancel: true,
                    closeOnConfirm: true
                },  
                function(isConfirm) { 
                    if (isConfirm) {
                        myResolve(true);
                    } else {
                        myReject(false);
                    }
                })
            }else{
                myResolve(true)
            }
        });

    respuestaSweet.then(
        function(value){ 
            if(value) {
                actualizarEquipo();
            }  
        }
    ) 
}

function actualizarEquipo(){
    var form = document.getElementById('formulario');
    if(!form.checkValidity()) {
        form.querySelector('#validate').click();
    } else {
        $.ajax({
            type: 'POST',
            url: 'equipoActualizar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    InventarioID : document.getElementById("InventarioID").value,
                    CodigoInventario : document.getElementById("CodigoInventario").value,
                    CategoriaID : document.getElementById("CategoriaID").value,
                    FabricanteID : document.getElementById("FabricanteID").value,
                    Modelo : document.getElementById("Modelo").value,
                    Serie : document.getElementById("Serie").value,
                    Descripcion : document.getElementById("Descripcion").value,
                    SucursalID : document.getElementById("SucursalID").value,
                    ProveedorID : document.getElementById("ProveedorID").value,
                    EstadoID : document.getElementById("EstadoID").value,
                    FechaCompra : document.getElementById("FechaCompra").value,
                    FechaUltimoSoporte : document.getElementById("FechaUltimoSoporte").value,
                    Notas : document.getElementById("Notas").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('Se ha actualizado el equipo exitosamente.');
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se actualizó el equipo. Este código alfanumérico ya existe.');
            }
        });
    }
}

function desactivarEquipo(){
    var form = document.getElementById('formulario');
    let respuestaSweet = new Promise(
        function(myResolve, myReject) { 
            swal({  
                title: "¿Desactivar el equipo?",  
                text: "Al desactivarlo el equipo se desasignará de cualquier empleado al que esté asignado.",
                showCancelButton: true,  
                confirmButtonColor: '#dc3545', 
                confirmButtonTextColor: 'white',  
                confirmButtonText: "¡Desactivar!",  
                cancelButtonText: "Cancelar",  
                closeOnConfirm: true,  
                closeOnCancel: true  
            },  
            function(isConfirm) {
                if (isConfirm) {
                    myResolve(true);
                } else {
                    myReject(false);
                }
            }) 
        }
    );

    respuestaSweet.then(
        function(value){ 
            if(value) {
                $.ajax({
                    type: 'POST',
                    url: 'equipoDesactivar/',
                    data: {
                            "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            InventarioID : document.getElementById("InventarioID").value,
                            usuario : document.getElementById("usuario").value,
                            device : document.getElementById("device").value
                        },
                    success: function(r) {
                        showSuccessMessage('Se ha desactivado el equipo exitosamente.');
                        form.reset();
                        document.getElementById("EstadoID").value = 2
                        $('html, body').animate({ scrollTop: 0 }, 'fast');
                    },
                    error: function(r) {
                        showErrorMessage('No se desactivó el equipo, intente más tarde.');
                    }
                });
            }  
        }
    ) 
}

function cargarImagen(tipoCodigo){
    var img = document.createElement("IMG");
    var nombre = document.getElementById("CodigoInventario").value;
    const childToReplace = document.getElementById("imagenCodigo");
    var padre = childToReplace.parentNode;
    img.src = ruta + "Cod-"+ tipoCodigo + nombre + ".png";
    img.style.maxHeight = '180px';
    img.style.maxWidth = '280px';
    img.id = 'imagenCodigo';
    img.className = 'center'
    padre.replaceChild(img, childToReplace);
}

function cargarNoCodeImagen(){
    var img = document.createElement("IMG");
    const childToReplace = document.getElementById("imagenCodigo");
    var padre = childToReplace.parentNode;
    img.src = ruta + "noCode.PNG";
    img.style.maxHeight = '180px';
    img.style.maxWidth = '280px';
    img.id = 'imagenCodigo';
    img.className = 'center'
    padre.replaceChild(img, childToReplace);
}

function generarBarras(){
    if (document.getElementById('CodigoInventario').value.length == 0) { 
        showErrorMessage('Debe rellenar el código alfanumérico para generar un código de barras.');
        document.getElementById('CodigoInventario').focus();
        return false
    } else {
        $.ajax({
            type: 'POST',
            url: 'codigoBarras/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    CodigoInventario : document.getElementById("CodigoInventario").value
                },
            success: function(r) {
                cargarImagen('B');
                var codigoTexto = "B" + document.getElementById('CodigoInventario').value;
                document.getElementById('CodigoBarra').value = codigoTexto;
                showSuccessMessage('Código generado correctamente, presione la imagen para descargarlo.');
            },
            error: function(r) {
                document.getElementById('CodigoBarra').value = "sincodigo";
                cargarNoCodeImagen();
                showErrorMessage('No se generó el código pues el código alfanumérico ingresado ya existe.');
            }
        });
    } 
}

function generarQR(){
    if (document.getElementById('CodigoInventario').value.length == 0) { 
        showErrorMessage('Debe rellenar el código alfanumérico para generar un código QR.');
        document.getElementById('CodigoInventario').focus();
        return false
    } else {
        $.ajax({
            type: 'POST',
            url: 'codigoQR/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    CodigoInventario : document.getElementById("CodigoInventario").value
                },
            success: function(r) {
                cargarImagen('QR');
                var codigoTexto = "QR" + document.getElementById('CodigoInventario').value;
                document.getElementById('CodigoBarra').value = codigoTexto;
                showSuccessMessage('Código generado correctamente, presione la imagen para descargarlo.');
            },
            error: function(r) {
                document.getElementById('CodigoBarra').value = "sincodigo";
                cargarNoCodeImagen();
                showErrorMessage('No se generó el código pues el código alfanumérico ingresado ya existe.');
            }
        });
    } 
}