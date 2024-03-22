from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
# Create your models here.


class Campeonato(BaseModel):
    nombre=models.CharField(max_length=250 , null=True)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    tipo=models.CharField(max_length=200)
    lugar=models.CharField(max_length=500)
    historical=HistoricalRecords()


    class Meta:
        verbose_name='Campeonato'
        verbose_name_plural='Campeonatos'

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by=value    


    def __str__(self) -> str:
        return self.nombre 



class Grupos(BaseModel):
    nombre=models.CharField(max_length=150 , blank=False,null=False,unique=True)
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
        verbose_name='Grupo'
        verbose_name_plural='Grupos'

