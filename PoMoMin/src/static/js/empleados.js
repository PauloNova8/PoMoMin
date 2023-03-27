function cargarPuestos() {
    cargarJefes()
    if ($('#PuestoIDEmpleado').length){
        puestoIDEmpleado = document.getElementById("PuestoIDEmpleado").value;
    } else {
        puestoIDEmpleado = '';
    }
    if ($('#DepartamentoID').length){
        deptoID = document.getElementById("DepartamentoID").value;
    } else {
        deptoID = '';
    }
    if(document.getElementById("DepartamentoID").value == ''){
        $('#PuestoID').html("<option value=''>Seleccione una opción</option><option value=''>--Debe seleccionar un departamento para seleccionar un puesto--</option>");
    } else {
        $.ajax({
            type: "POST",
            url: "cargarPuestos/",
            data: {
                "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                'DepartamentoID' : deptoID,
                'PuestoID' : puestoIDEmpleado
            },
            success: function (respuesta) {
                $('#PuestoID').html(respuesta);
            }
        });
        return false;
    }
}

function cargarJefes() {
    if ($('#SucursalID').length){
        sucursalID = document.getElementById("SucursalID").value;
    } else {
        sucursalID = '';
    }
    if ($('#DepartamentoID').length){
        deptoID = document.getElementById("DepartamentoID").value;
    } else {
        deptoID = '';
    }
    if ($('#ReportaAEmpleado').length){
        reportaAEmpleado = document.getElementById("ReportaAEmpleado").value;
    } else {
        reportaAEmpleado = '';
    }
    if(document.getElementById("SucursalID").value == '' || document.getElementById("DepartamentoID").value == ''){
        $('#ReportaA').html("<option value=''>Seleccione una opción</option><option value='Ninguno'>Ninguno</option>");
    } else {
        $.ajax({
            type: "POST",
            url: "cargarJefes/",
            data: {
                "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                'SucursalID' : sucursalID,
                'DepartamentoID' : deptoID,
                'ReportaAEmpleado' : reportaAEmpleado
            },
            success: function (respuesta) {
                $('#ReportaA').html(respuesta);
            }
        });
        return false;
    }
}

function insertarEmpleado() {
    var form = document.getElementById('formulario');
    var nacimiento = new Date(document.getElementById("FechaNacimiento").value);
    var contratacion = new Date(document.getElementById("FechaAlta").value);
    if (nacimiento.getTime() > contratacion.getTime()) {
        showErrorMessage('La fecha de contratación no puede ser antes de la fecha de nacimiento.');
        return false
    }
    
    if (document.getElementById("FechaBaja").value.length != 0) { 
        var d1 = new Date(document.getElementById("FechaAlta").value);
        var d2 = new Date(document.getElementById("FechaBaja").value);
        if (d1.getTime() > d2.getTime()) {
            showErrorMessage('La fecha de baja no puede ser antes de la fecha de contratacion.');
            return false
        }
    }
    
    if(!form.checkValidity()) {
        form.querySelector('#validate').click();
    } else {
        $.ajax({
            type: 'POST',
            url: 'empleadoInsertar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    Nombres : document.getElementById("Nombres").value,
                    Apellidos : document.getElementById("Apellidos").value,
                    Identificacion : document.getElementById("Identificacion").value,
                    SucursalID : document.getElementById("SucursalID").value,
                    PuestoID : document.getElementById("PuestoID").value,
                    ReportaA : document.getElementById("ReportaA").value,
                    TelefonoCelular : document.getElementById("TelefonoCelular").value,
                    TelefonoTrabajo : document.getElementById("TelefonoTrabajo").value,
                    Direccion : document.getElementById("Direccion").value,
                    Genero : document.getElementById("Genero").value,
                    FechaNacimiento : document.getElementById("FechaNacimiento").value,
                    FechaAlta : document.getElementById("FechaAlta").value,
                    FechaBaja : document.getElementById("FechaBaja").value,
                    EstadoID : document.getElementById("EstadoID").value,
                    Notas : document.getElementById("Notas").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('El empleado se ha registrado exitosamente.');
                form.reset();
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se registró el empleado. El número de identidad ya existe.');
            }
        });
    } 
}

function permitirBaja(){
    if(document.getElementById("EstadoID").value == 2) {
        document.getElementById("FechaBaja").readOnly = false;
    } else {
        document.getElementById("FechaBaja").value = '';
        document.getElementById("FechaBaja").readOnly = true;
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

$(document).ready(function(){
    $('#TablaEmpleados').DataTable( {
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
});

$(document).ready(function () {
    cargarPuestos();
    cargarJefes();
})

function validaciones(){
    var nacimiento = new Date(document.getElementById("FechaNacimiento").value);
    var contratacion = new Date(document.getElementById("FechaAlta").value);
    if (nacimiento.getTime() > contratacion.getTime()) {
        showErrorMessage('La fecha de contratación no puede ser antes de la fecha de nacimiento.');
        return false
    }
    
    if (document.getElementById("FechaBaja").value.length != 0) { 
        var d1 = new Date(document.getElementById("FechaAlta").value);
        var d2 = new Date(document.getElementById("FechaBaja").value);
        if (d1.getTime() > d2.getTime()) {
            showErrorMessage('La fecha de baja no puede ser antes de la fecha de contratacion.');
            return false
        }
    }

    let respuestaSweet = new Promise(
        function(myResolve, myReject) { 
            if (document.getElementById("EstadoID").value == 2) {
                swal({  
                    title: "¿Actualizar el empleado a 'Inactivo'?",  
                    text: "Al desactivarlo todo el equipo/mobiliario que el empleado tenga asignado se le desasignará automáticamente.",
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
                actualizarEmpleado();
            }  
        }
    ) 
}

function actualizarEmpleado(){
    var form = document.getElementById('formulario');
    if(!form.checkValidity()) {
        form.querySelector('#validate').click();
    } else {
        $.ajax({
            type: 'POST',
            url: 'empleadoActualizar/',
            data: {
                    "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    EmpleadoID : document.getElementById("EmpleadoID").value,
                    Nombres : document.getElementById("Nombres").value,
                    Apellidos : document.getElementById("Apellidos").value,
                    Identificacion : document.getElementById("Identificacion").value,
                    SucursalID : document.getElementById("SucursalID").value,
                    PuestoID : document.getElementById("PuestoID").value,
                    ReportaA : document.getElementById("ReportaA").value,
                    TelefonoCelular : document.getElementById("TelefonoCelular").value,
                    TelefonoTrabajo : document.getElementById("TelefonoTrabajo").value,
                    Direccion : document.getElementById("Direccion").value,
                    Genero : document.getElementById("Genero").value,
                    FechaNacimiento : document.getElementById("FechaNacimiento").value,
                    FechaAlta : document.getElementById("FechaAlta").value,
                    FechaBaja : document.getElementById("FechaBaja").value,
                    EstadoID : document.getElementById("EstadoID").value,
                    Notas : document.getElementById("Notas").value,
                    usuario : document.getElementById("usuario").value,
                    device : document.getElementById("device").value
                },
            success: function(r) {
                showSuccessMessage('El empleado se ha actualizado exitosamente.');
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            },
            error: function(r) {
                showErrorMessage('No se actualizó el empleado. Este número de identidad ya existe.');
            }
        });
    }
}

function desactivarEmpleado(){
    var form = document.getElementById('formulario');
    let respuestaSweet = new Promise(
        function(myResolve, myReject) { 
            swal({  
                title: "¿Desactivar a este empleado?",  
                text: "Al desactivarlo todo el equipo/mobiliario que el empleado tenga asignado se le desasignará automáticamente.",
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
                    url: 'empleadoDesactivar/',
                    data: {
                            "csrfmiddlewaretoken" : document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            EmpleadoID : document.getElementById("EmpleadoID").value,
                            usuario : document.getElementById("usuario").value,
                            device : document.getElementById("device").value
                        },
                    success: function(r) {
                        showSuccessMessage('El empleado se ha desactivado exitosamente.');
                        form.reset();
                        document.getElementById("EstadoID").value = 2

                        var today = new Date();
                        var dd = String(today.getDate()).padStart(2, '0');
                        var mm = String(today.getMonth() + 1).padStart(2, '0'); //Los meses en JS van del 0 hasta el 11, igual que mi IQ
                        var yyyy = today.getFullYear();
                        document.getElementById("FechaBaja").value = yyyy + '-' + mm + '-' + dd;

                        $('html, body').animate({ scrollTop: 0 }, 'fast');
                    },
                    error: function(r) {
                        showErrorMessage('No se desactivó el empleado, intente más tarde.');
                    }
                });
            }  
        }
    ) 
}