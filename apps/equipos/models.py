from django.db import models
from apps.base.models import BaseModel


class Equipos(BaseModel):
    nombre=models.CharField(max_length=150 , blank=False,null=False,unique=True)
    delegado=models.CharField(max_length=150 , blank=False , null=True)
    foto_delegado=models.ImageField(upload_to='img_delegados',null=True, blank=True)
    logo_equipo=models.ImageField(upload_to='logo_equipos' , null=True , blank=True)

    def __str__(self) -> str:
        return f"{self.nombre}"

    
    class Meta:
        verbose_name='Equipo'
        verbose_name_plural='Equipos'





