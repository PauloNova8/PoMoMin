function insertarProveedor() {
    var form = document.getElementById('formulario');
    if(!form.checkValidity()) {
            form.querySelector('#validate').click();
    } else {
        $.ajax({
            type: 'POST',
            url: 'proveedorInsertar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    Nombre : document.getElementById("Nombre").value,
                    Descripcion : document.getElementById("Descripcion").value,
                    Direccion : document.getElementById("Direccion").value,
                    Telefono : document.getElementById("Telefono").value,
                    NombreContacto : document.getElementById("NombreContacto").value,
                    Notas : document.getElementById("Notas").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('Se ha registrado este proveedor exitosamente.');
                form.reset();
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se registró el proveedor. Se presentó un error interno.');
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
    $('#TablaProveedor').DataTable( {
        "pageLength" : 10,
        "order": [[ 0, "asc" ]],
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
    
    document.getElementById("TablaProveedor_filter").
    querySelector('label').
    querySelector('input').id = "barraBusqueda";
});

function validaciones(){
    let respuestaSweet = new Promise(
        function(myResolve, myReject) { 
            if (document.getElementById("Activo").value == 0) {
                swal({  
                    title: "¿Actualizar el proveedor a 'Inactivo'?",  
                    text: "Al desactivarlo, el proveedor seguirá ligado a cualquier registro en el que se haga referencia.",
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
                actualizarProveedor();
            }  
        }
    ) 
}

function actualizarProveedor(){
    var form = document.getElementById('formulario');
    if(!form.checkValidity()) {
        form.querySelector('#validate').click();
    } else {
        $.ajax({
            type: 'POST',
            url: 'proveedorActualizar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    ProveedorID : document.getElementById("ProveedorID").value,
                    Nombre : document.getElementById("Nombre").value,
                    Activo : document.getElementById("Activo").value,
                    Descripcion : document.getElementById("Descripcion").value,
                    Direccion : document.getElementById("Direccion").value,
                    Telefono : document.getElementById("Telefono").value,
                    NombreContacto : document.getElementById("NombreContacto").value,
                    Notas : document.getElementById("Notas").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('El proveedor se ha actualizado exitosamente.');
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se actualizó el proveedor. Ha surgido un error interno.');
            }
        });
    }
}

function desactivarProveedor(){
    var form = document.getElementById('formulario');
    let respuestaSweet = new Promise(
        function(myResolve, myReject) { 
            swal({  
                title: "¿Desactivar este proveedor?",  
                text: "Al desactivarlo, el proveedor seguirá ligado a cualquier registro en el que se haga referencia.",
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
                    url: 'proveedorDesactivar/',
                    data: {
                            "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            ProveedorID : document.getElementById("ProveedorID").value,
                            usuario : document.getElementById("usuario").value,
                            device : document.getElementById("device").value
                        },
                    success: function(r) {
                        showSuccessMessage('El proveedor se ha desactivado exitosamente.');
                        form.reset();
                        document.getElementById("Activo").value = 0
                        $('html, body').animate({ scrollTop: 0 }, 'fast');
                    },
                    error: function(r) {
                        showErrorMessage('No se desactivó el proveedor, intente más tarde.');
                    }
                });
            }  
        }
    ) 
}


//CREACION DE MASCARAS PARA LOS INPUTS
document.addEventListener('DOMContentLoaded', () => {
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
});
