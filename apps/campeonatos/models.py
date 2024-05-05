from django.db import models
from apps.base.models import BaseModel
from apps.equipos.models import Equipos


class Campeonato(BaseModel):
    nombre=models.CharField(max_length=250 , unique=True)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    tipo=models.CharField(max_length=200)#libre master o juvenil
    lugar=models.CharField(max_length=500)

    class Meta:
        verbose_name='Campeonato'
        verbose_name_plural='Campeonatos'
        db_table="campeonatos"

    def __str__(self) -> str:
        return self.nombre 



class Grupos(BaseModel):
    nombre=models.CharField(max_length=150 , blank=False,null=False,unique=True)
    campeonato=models.ForeignKey(Campeonato,on_delete=models.CASCADE,default=None)

    def __str__(self) -> str:
        return self.nombre

    
    class Meta:
        verbose_name='Grupo'
        verbose_name_plural='Grupos'
        db_table='grupos'




class EquipoGrupo(BaseModel):

    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.equipo.nombre} - {self.grupo.nombre}"

    
    class Meta:
        verbose_name='Equipo_grupo'
        verbose_name_plural='Equipos_Grupos'
        db_table='Equipo_grupo'







class EquiposCampeonatos(BaseModel):
    campeonato=models.ForeignKey(Campeonato,on_delete=models.CASCADE)
    equipo=models.ForeignKey(Equipos,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Equipo {self.equipo.nombre} - Campeonato {Campeonato.nombre}"
    

    class Meta:
        verbose_name='Campeonato_Equipo'
        verbose_name_plural='Campeonato_Equipos'
        db_table='equipos_campeonato'