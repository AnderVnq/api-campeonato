from django.db import models
from django.db.models import Model
from apps.base.models import BaseModel
from apps.campeonatos.models import Grupos
from simple_history.models import HistoricalRecords
# Create your models here.





# class Grupos(BaseModel):
#     nombre=models.CharField(max_length=150 , blank=False,null=False,unique=True)
#     historical=HistoricalRecords()

#     @property
#     def _history_user(self):
#         return self.changed_by
    
#     @_history_user.setter
#     def _history_user(self,value):
#         self.changed_by=value

#     def __str__(self) -> str:
#         return self.nombre

    
#     class Meta:
#         verbose_name='Grupo'
#         verbose_name_plural='Grupos'





class Equipos(BaseModel):
    nombre=models.CharField(max_length=150 , blank=False,null=False,unique=True)
    delegado=models.CharField(max_length=150 , blank=False , null=True)
    foto_delegado=models.ImageField(upload_to='img_delegados',null=True, blank=True)
    logo_equipo=models.ImageField(upload_to='logo_equipos' , null=True , blank=True)
    grupos=models.ForeignKey(Grupos,on_delete=models.CASCADE, related_name='grupos')
    # historical=HistoricalRecords()



    # @property
    # def _history_user(self):
    #     return self.changed_by
    
    # @_history_user.setter
    # def _history_user(self,value):
    #     self.changed_by=value

    def __str__(self) -> str:
        return f"{self.nombre}"

    
    class Meta:
        verbose_name='Equipo'
        verbose_name_plural='Equipos'





