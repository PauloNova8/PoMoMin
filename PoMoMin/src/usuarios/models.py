from django.db import models

class showPerfiles(models.Model):
    PerfilID = models.IntegerField()
    NombrePerfil = models.CharField(max_length=100)
    Descripcion = models.CharField(max_length=150)
    class Meta:
        db_table = "PerfilesUsuario"

class showEstados(models.Model):
    EstadoID = models.IntegerField()
    Estado = models.CharField(max_length=100)
    Descripcion = models.CharField(max_length=150)
    class Meta:
        db_table = "EstadosUsuario"


class showUsuarios(models.Model):
    UsuarioID = models.IntegerField()
    Usuario = models.CharField(max_length=200)
    Token = models.CharField(max_length=300)
    PerfilID = models.IntegerField(default=None)
    NombrePerfil = models.CharField(max_length=100)
    FechaCreacion = models.CharField(max_length=100, default=None)
    FechaUltimaActualizacion = models.CharField(max_length=100, default=None)
    EstadoID = models.IntegerField(default=None)
    Estado = models.CharField(max_length=100, default=None)
    class Meta:
        db_table = "v_Usuarios"