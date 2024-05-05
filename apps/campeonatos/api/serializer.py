from django.db.models import Count 
from rest_framework import serializers
from apps.campeonatos.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.encuentros.models import Goles
from apps.encuentros.api.serializers.general_serializer import GolesSerializer
from apps.equipos.api.serializers import EquipoSerializer

class CampeonatoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Campeonato
        exclude=['state','created_date','modified_date','deleted_date']
        


class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Añadir expires y created al diccionario data
        data['expires'] = refresh.access_token.get('exp')
        data['created'] = refresh.access_token.get('iat')

        return data



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
    


class EquiposCampeonatosSerializer(serializers.ModelSerializer):
    equipo = EquipoSerializer(many=True)
    #campeonato = serializers.SerializerMethodField()

    class Meta:
        model = EquiposCampeonatos
        exclude = ['state', 'created_date', 'modified_date', 'deleted_date']

    def to_representation(self, instance):

        campeonato=instance[0]
        campeonato_representation={
            'id':campeonato.campeonato.id,
            'nombre':campeonato.campeonato.nombre,
            'fecha_inicio':campeonato.campeonato.fecha_inicio,
            'fecha_fin':campeonato.campeonato.fecha_fin,
            'tipo':campeonato.campeonato.tipo,
            'lugar':campeonato.campeonato.lugar,
        }
        print("representation")
        for x in instance:
            print(x.equipo.nombre , x.equipo.delegado)

        equipos_representation=[
            {
                'id': i.equipo.id,
                'nombre': i.equipo.nombre,
                'delegado': i.equipo.delegado,
                'foto_delegado': i.equipo.foto_delegado.url if i.equipo.foto_delegado != '' and i.equipo.foto_delegado else '',  # Ajusta según la lógica de tu aplicación
                'logo_equipo':i.equipo.logo_equipo.url if i.equipo.logo_equipo !='' else '',
            }
            for i in instance
        ]

        representation={
            'campeonato':campeonato_representation,
            'equipos':equipos_representation
        }

        return representation
