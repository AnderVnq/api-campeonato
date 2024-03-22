from django.db.models import Count 
from rest_framework import serializers
from apps.campeonatos.models import Campeonato
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.encuentros.models import Goles
from apps.encuentros.api.serializers.general_serializer import GolesSerializer
from apps.jugadores.models import Jugadores
class CampeonatoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Campeonato
        exclude=['state','created_date','modified_date','deleted_date']
        


class CustomTokenSerializer(TokenObtainPairSerializer):
    pass




class TopGolesSerializer(serializers.ModelSerializer):
    
    goles=GolesSerializer(many=True)

    class Meta:
        model=Campeonato
        exclude=['state','created_date','modified_date','deleted_date']


    def to_representation(self, instance):

        print(instance.id)
        
        jugadores_con_goles = Goles.objects.filter(encuentro__campeonato_id=instance.id).values(
            'jugador__nombre',
            'jugador__equipo__nombre',
            'jugador__imagen_dni'
        ).annotate(total_goles=Count('id')).order_by('-total_goles')



        # jugadores_con_partidos = Jugadores.objects.annotate(
        #     total_partidos_jugados=Count('goles_jugador__encuentro', distinct=True)
        # )

        # # Ahora, puedes acceder a la cantidad de partidos jugados por cada jugador
        # for jugador in jugadores_con_partidos:
        #     print(f'{jugador.nombre} ha jugado {jugador.total_partidos_jugados} partidos.')
        # Crea la representación final
        top_representation = [
            {
                'rank': rank,
                'nombre': jugador['jugador__nombre'],
                'equipo': jugador['jugador__equipo__nombre'],
                'img_jugador':jugador['jugador__imagen_dni'],
                'goles': jugador['total_goles'],

                
            }
            for rank, jugador in enumerate(jugadores_con_goles,start=1)
            
        ]

        return {
            'campeonato_id':instance.id,
            'nombre':instance.nombre,
            'top-goles':top_representation
        }