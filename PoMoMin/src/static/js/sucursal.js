function insertarSucursal() {
    var form = document.getElementById('formulario');
    if(!form.checkValidity()) {
            form.querySelector('#validate').click();
    } else {
        $.ajax({
            type: 'POST',
            url: 'sucursalInsertar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    Nombre : document.getElementById("Nombre").value,
                    Direccion : document.getElementById("Direccion").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('Se ha registrado esta sucursal exitosamente.');
                form.reset();
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se registró la sucursal. Se presentó un error interno.');
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
    $('#TablaSucursal').DataTable( {
        "pageLength" : 10,
        "order": [[ 0, "asc" ]],
        "aaSorting": [],
            columnDefs: [{
            orderable: false,
            targets: 3
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
    
    document.getElementById("TablaSucursal_filter").
    querySelector('label').
    querySelector('input').id = "barraBusqueda";
});

function validaciones(){
    let respuestaSweet = new Promise(
        function(myResolve, myReject) { 
            if (document.getElementById("Activo").value == 0) {
                swal({  
                    title: "¿Actualizar la sucursal a 'Inactivo'?",  
                    text: "Al desactivarla, la sucursal seguirá ligada a cualquier registro a la que haga referencia.",
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
            } else{
                myResolve(true)
            }
        });

    respuestaSweet.then(
        function(value){ 
            if(value) {
                actualizarSucursal();
            }  
        }
    ) 
}

function actualizarSucursal(){
    var form = document.getElementById('formulario');
    if(!form.checkValidity()) {
        form.querySelector('#validate').click();
    } else {
        $.ajax({
            type: 'POST',
            url: 'sucursalActualizar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    SucursalID : document.getElementById("SucursalID").value,
                    Nombre : document.getElementById("Nombre").value,
                    Activo : document.getElementById("Activo").value,
                    Direccion : document.getElementById("Direccion").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('La sucursal se ha actualizado exitosamente.');
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se actualizó la sucursal. Ha surgido un error interno.');
            }
        });
    }
}

function desactivarSucursal(){
    var form = document.getElementById('formulario');
    let respuestaSweet = new Promise(
        function(myResolve, myReject) { 
            swal({  
                title: "¿Desactivar la sucursal?",  
                text: "Al desactivarla, la sucursal seguirá ligada a cualquier registro a la que haga referencia.",
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
                    url: 'sucursalDesactivar/',
                    data: {
                            "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            SucursalID : document.getElementById("SucursalID").value,
                            usuario : document.getElementById("usuario").value,
                            device : document.getElementById("device").value
                        },
                    success: function(r) {
                        showSuccessMessage('La sucursal se ha desactivado exitosamente.');
                        form.reset();
                        document.getElementById("Activo").value = 0
                        $('html, body').animate({ scrollTop: 0 }, 'fast');
                    },
                    error: function(r) {
                        showErrorMessage('No se desactivó la sucursal, intente más tarde.');
                    }
                });
            }  
        }
    ) 
}
