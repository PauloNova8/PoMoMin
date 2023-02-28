from django.db import models

# Create your models here.

class showDepartamentos(models.Model):
    DepartamentoID = models.IntegerField()
    Nombre = models.CharField(max_length=100)
    class Meta:
        db_table = "Departamentos"


class showPuestos(models.Model):
    PuestoID = models.IntegerField()
    Nombre = models.CharField(max_length=100)
    DepartamentoID = models.IntegerField()
    class Meta:
        db_table = "Puestos"


class showEmpleados(models.Model):
    EmpleadoID = models.IntegerField()
    Nombre = models.CharField(max_length=100)
    Apellido = models.CharField(max_length=100)
    SucursalID = models.IntegerField()
    PuestoID = models.IntegerField()
    PuestoTexto = models.CharField(max_length=200)
    Nombres = models.CharField(max_length=100, default=None)
    Apellidos = models.CharField(max_length=100, default=None)
    NombreCompleto = models.CharField(max_length=200, default=None)
    Sucursal = models.CharField(max_length=100, default=None)
    Identificacion = models.CharField(max_length=100, default=None)
    ReportaA  = models.IntegerField(default=None)
    TelefonoCelular = models.CharField(max_length=100, default=None)
    TelefonoTrabajo = models.CharField(max_length=100, default=None)
    Direccion = models.CharField(max_length=150, default=None)
    Genero = models.CharField(max_length=15, default=None)
    FechaNacimiento  = models.CharField(max_length=100, default=None)
    FechaAlta = models.CharField(max_length=100, default=None)
    FechaBaja = models.CharField(max_length=100, default=None)
    EstadoID = models.IntegerField(default=None)
    Estado = models.CharField(max_length=100, default=None)
    Notas = models.TextField(max_length=100, default=None)
    Departamento = models.TextField(max_length=100, default=None)
    DepartamentoID = models.IntegerField(default=None)
    class Meta:
        db_table = "Empleados"


class showEstados(models.Model):
    EstadoID = models.IntegerField()
    Estado = models.CharField(max_length=100)
    class Meta:
        db_table = "EstadosEmpleado"