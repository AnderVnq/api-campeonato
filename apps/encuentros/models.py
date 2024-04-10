from django.db import models
from apps.base.models import BaseModel
from apps.equipos.models import Equipos
from simple_history.models import HistoricalRecords
from apps.campeonatos.models import Campeonato
from apps.jugadores.models import Jugadores
from apps.arbitros.models import Arbitro
# Create your models here.




class Encuentro(BaseModel):
    campeonato=models.ForeignKey(Campeonato,on_delete=models.CASCADE , related_name='encuentros')
    equipo_local=models.ForeignKey(Equipos,on_delete=models.CASCADE,related_name='equipo_local')
    equipo_visitante=models.ForeignKey(Equipos,on_delete=models.CASCADE,related_name='equipo_visitante')
    fecha=models.DateField()
    arbitros=models.ManyToManyField(Arbitro)
    # historical=HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by
    
    # @_history_user.setter
    # def _history_user(self,value):
    #     self.changed_by=value

    
    class Meta:
        verbose_name='Encuentro'
        verbose_name_plural='Encuentros'


    def __str__(self) -> str:
        return f'{self.id} -{self.equipo_local} vs {self.equipo_visitante}'


class Goles(BaseModel):
    encuentro = models.ForeignKey(Encuentro, on_delete=models.CASCADE , related_name='goles')
    jugador = models.ForeignKey(Jugadores, on_delete=models.CASCADE , related_name='goles_jugador')
    minuto=models.PositiveIntegerField()
    # historical=HistoricalRecords()


    # @property
    # def _history_user(self):
    #     return self.changed_by
    
    # @_history_user.setter
    # def _history_user(self,value):
    #     self.changed_by=value

    
    class Meta:
        verbose_name='Goles'
        verbose_name_plural='Goles'

    def __str__(self) -> str:
        return f"{self.jugador.nombre}-{self.jugador.equipo.nombre} - min {self.minuto}"

class Sancion(BaseModel):
    encuentro = models.ForeignKey(Encuentro, on_delete=models.CASCADE , related_name='sanciones')
    jugador = models.ForeignKey(Jugadores, on_delete=models.CASCADE , related_name='sancion_jugador')
    tipo = models.CharField(max_length=50)  # Tarjeta amarilla, tarjeta roja, etc.
    minuto = models.PositiveIntegerField()
    motivo = models.TextField()
    # historical=HistoricalRecords()


    # @property
    # def _history_user(self):
    #     return self.changed_by
    
    # @_history_user.setter
    # def _history_user(self,value):
    #     self.changed_by=value
    class Meta:
        verbose_name='Sancion'
        verbose_name_plural='Sanciones'

    def __str__(self) -> str:
        return f"{self.tipo}-{self.jugador.nombre}"


