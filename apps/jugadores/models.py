from django.db import models
from apps.base.models import BaseModel
from apps.equipos.models import Equipos
from simple_history.models import HistoricalRecords
# Create your models here.


# class Estadisticas(BaseModel):





class Jugadores(BaseModel):

    nombre=models.CharField(max_length=100)
    apellido_pat=models.CharField(max_length=100)
    apellido_mat=models.CharField(max_length=100,default=None)
    fecha_nacimiento=models.DateField(null=False , blank=False)
    posicion_jugador=models.CharField(max_length=200)
    imagen_dni=models.ImageField(upload_to='jugadores/dni',blank=True,null=True)
    equipo=models.ForeignKey(Equipos,on_delete=models.CASCADE , related_name='jugadores')
    foto=models.ImageField(upload_to='jugadores/foto',blank=True,null=True)
    direccion=models.CharField(max_length=150 , null=True)


    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        verbose_name='Jugador'
        verbose_name_plural='Jugadores'













