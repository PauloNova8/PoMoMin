function insertarUsuario() {
    var form = document.getElementById('formulario');
    if (document.getElementById("Clave").value.length != 0) { 
        var clave1 = document.getElementById("Clave1").value;
        var clave = document.getElementById("Clave").value;
        if (clave1 != clave) {
            showErrorMessage('Las contraseñas no coinciden.');
            document.getElementById("Clave1").focus();
            return false
        }
    }
    if(!form.checkValidity()) {
            form.querySelector('#validate').click();
    } else {
        $.ajax({
            type: 'POST',
            url: 'usuarioInsertar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    Usuario : document.getElementById("Usuario").value,
                    Token : btoa(document.getElementById("Clave").value),
                    PerfilID : document.getElementById("PerfilID").value,
                    EstadoID : document.getElementById("EstadoID").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('Se ha registrado el usuario exitosamente.');
                form.reset();
                cargarNoCodeImagen();
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se registró el usuario. Este nombre de usuario ya existe.');
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
    $('#TablaUsuario').DataTable( {
        "pageLength" : 10,
        "order": [[ 2, "desc" ]],
        "aaSorting": [],
            columnDefs: [{
            orderable: false,
            targets: 5
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
    
    document.getElementById("TablaUsuario_filter").
    querySelector('label').
    querySelector('input').id = "barraBusqueda";
});

function validaciones(){
    if (document.getElementById("Clave0").value.length != 0) {
        if(document.getElementById("Clave1").value.length == 0){
            showErrorMessage("Si desea cambiar la contraseña debe llenar todos los campos relacionados");
            document.getElementById("Clave1").focus();
            return false
        }
        if(document.getElementById("Clave").value.length == 0){
            showErrorMessage("Si desea cambiar la contraseña debe llenar todos los campos relacionados");
            document.getElementById("Clave").focus();
            return false
        }
        var token = document.getElementById("token").value; 
        var clave0 = document.getElementById("Clave0").value;
        var clave1 = document.getElementById("Clave1").value;
        var clave = document.getElementById("Clave").value;
        if (clave0 != atob(token)) {
            showErrorMessage('La contraseña anterior no es válida.');
            document.getElementById("Clave0").focus();
            return false
        } else if (clave0 == clave1) {
            showErrorMessage('La nueva contraseña no puede ser igual a la anterior.');
            document.getElementById("Clave1").focus();
            return false
         } else if (clave1 != clave) {
            showErrorMessage('La nueva contraseña no coincide con la comprobación.');
            document.getElementById("Clave1").focus();
            return false
        }
    }

    let respuestaSweet = new Promise(
        function(myResolve, myReject) { 
            if (document.getElementById("EstadoID").value == 2) {
                swal({  
                    title: "¿Actualizar el usuario a 'Inactivo'?",  
                    text: "Al desactivarlo, este usuario no podrá iniciar sesión nuevamente.",
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
                    title: "¿Actualizar el usuario a 'Suspendido'?",  
                    text: "Al suspenderlo, este usuario no podrá iniciar sesión temporalmente hasta que se vuelva a marcar como activo.",
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
            }else{
                myResolve(true)
            }
        });
        

    respuestaSweet.then(
        function(value){ 
            if(value) {
                actualizarUsuario();
            }  
        }
    ) 
}

function actualizarUsuario(){
    var form = document.getElementById('formulario');
    if(!form.checkValidity()) {
        form.querySelector('#validate').click();
    } else {
        $.ajax({
            type: 'POST',
            url: 'usuarioActualizar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    UsuarioID : document.getElementById("UsuarioID").value,
                    Token : btoa(document.getElementById("Clave").value),
                    PerfilID : document.getElementById("PerfilID").value,
                    EstadoID : document.getElementById("EstadoID").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('El usuario se ha actualizado exitosamente.');
                document.getElementById("Clave0").value = '';
                document.getElementById("Clave1").value = '';
                document.getElementById("Clave").value = '';
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se actualizó el usuario. Ha surgido un error interno.');
            }
        });
    }
}

function desactivarUsuario(){
    var form = document.getElementById('formulario');
    let respuestaSweet = new Promise(
        function(myResolve, myReject) { 
            swal({  
                title: "¿Desactivar el usuario?",  
                text: "Al desactivarlo, este usuario no podrá iniciar sesión nuevamente.",
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
                    url: 'usuarioDesactivar/',
                    data: {
                            "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            UsuarioID : document.getElementById("UsuarioID").value,
                            usuario : document.getElementById("usuario").value,
                            device : document.getElementById("device").value
                        },
                    success: function(r) {
                        showSuccessMessage('El usuario se ha desactivado exitosamente.');
                        form.reset();
                        document.getElementById("EstadoID").value = 2
                        $('html, body').animate({ scrollTop: 0 }, 'fast');
                    },
                    error: function(r) {
                        showErrorMessage('No se desactivó el usuario, intente más tarde.');
                    }
                });
            }  
        }
    ) 
}

