from django.db import models


class showBitacora(models.Model):
    NoRegistro = models.IntegerField()
    Usuario = models.CharField(max_length=100)
    FechaHoraEvento = models.CharField(max_length=100)
    TipoEvento = models.CharField(max_length=50)
    EstadoEvento = models.CharField(max_length=50)
    Descripcion = models.CharField(max_length=250)
    Dispositivo = models.CharField(max_length=200)
    class Meta:
        db_table = "Bitacora"