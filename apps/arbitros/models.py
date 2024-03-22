from django.db import models
from apps.base.models import BaseModel
from simple_history.models import HistoricalRecords
# Create your models here.

    
class Arbitro(BaseModel):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento=models.DateField()
    num_telefono=models.CharField(max_length=10)
    tipo = models.CharField(max_length=100)#principal o secundario 
    historical=HistoricalRecords()

    class Meta:
        verbose_name='Arbitro'
        verbose_name_plural='Arbitros'


    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by=value    

    def __str__(self) -> str:
        return self.nombre
