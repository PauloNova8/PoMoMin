import json
from django.db import models

# Create your models here.
class showCategorias(models.Model):
    CategoriaID = models.IntegerField()
    Categoria = models.CharField(max_length=100)
    AplicaA = models.CharField(max_length=1)
    class Meta:
        db_table = "Categorias"


class showFabricantes(models.Model):
    FabricanteID = models.IntegerField()
    Nombre = models.CharField(max_length=100)
    Activo = models.IntegerField()
    class Meta:
        db_table = "Fabricantes"


class showEstados(models.Model):
    EstadoID = models.IntegerField()
    Estado = models.CharField(max_length=100)
    class Meta:
        db_table = "EstadosInventario"


class showSucursales(models.Model):
    SucursalID = models.IntegerField()
    Nombre = models.CharField(max_length=100)
    Activo = models.IntegerField()
    class Meta:
        db_table = "Sucursales"


class showProveedores(models.Model):
    ProveedorID = models.IntegerField()
    Nombre = models.CharField(max_length=100)
    Activo = models.IntegerField()
    class Meta:
        db_table = "Proveedores"


class showInventario(models.Model):
    InventarioID = models.IntegerField()
    CodigoInventario = models.CharField(max_length=200)
    Categoria = models.CharField(max_length=100)
    Modelo = models.CharField(max_length=100)
    Serie = models.CharField(max_length=100)
    Fabricante = models.CharField(max_length=100)
    CategoriaID = models.IntegerField(default=None)
    FabricanteID = models.IntegerField(default=None)
    CodigoBarra = models.CharField(max_length=200, default=None)
    TipoInventarioID = models.IntegerField(default=None)
    Descripcion = models.CharField(max_length=150, default=None)
    SucursalID = models.IntegerField(default=None)
    Sucursal = models.CharField(max_length=100, default=None)
    AsignadoA = models.IntegerField(default=None)
    AsignadoNombre = models.CharField(max_length=200, default=None)
    ProveedorID = models.IntegerField(default=None)
    EstadoID = models.IntegerField(default=None)
    Estado = models.CharField(max_length=100, default=None)
    FechaCompra = models.CharField(max_length=100, default=None)
    FechaUtilMaxima =models.CharField(max_length=100, default=None)
    FechaUltimoSoporte =models.CharField(max_length=100, default=None)
    Notas = models.TextField(default=None) 
    class Meta:
        db_table = "Inventario"