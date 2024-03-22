from django.db import models
from apps.base.models import BaseModel
from apps.equipos.models import Equipos
from simple_history.models import HistoricalRecords
# Create your models here.


# class Estadisticas(BaseModel):





class Jugadores(BaseModel):

    nombre=models.CharField(max_length=100)
    apellidos=models.CharField(max_length=100)
    fecha_nacimiento=models.DateField(null=False , blank=False)
    posicion_jugador=models.CharField(max_length=200)
    imagen_dni=models.ImageField(upload_to='jugadores/dni',blank=True,null=True)
    equipo=models.ForeignKey(Equipos,on_delete=models.CASCADE , related_name='jugadores')
    foto=models.ImageField(upload_to='jugadores/foto',blank=True,null=True)
    direccion=models.CharField(max_length=150 , null=True)
    historical=HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by=value


    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        verbose_name='Jugador'
        verbose_name_plural='Jugadores'













