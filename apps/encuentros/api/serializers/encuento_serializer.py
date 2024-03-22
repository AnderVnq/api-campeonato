from apps.encuentros.models import Encuentro,Goles
from rest_framework import serializers
from apps.campeonatos.api.serializer import CampeonatoSerializer
from apps.equipos.api.serializers import EquipoSerializer
from apps.arbitros.api.serializer import ArbitroSerializer
from apps.jugadores.api.serializers import JugadorSerializer
from apps.encuentros.api.serializers.general_serializer import GolesSerializer



class EncuentroSerializer(serializers.ModelSerializer):

    class Meta:
        model=Encuentro
        exclude=['state','deleted_date','modified_date']

    def to_representation(self, instance):

        goles_local=instance.goles.filter(jugador__equipo=instance.equipo_local).count()
        goles_visitante=instance.goles.filter(jugador__equipo=instance.equipo_visitante).count()
        return {
            'id':instance.id,
            'campeonato': instance.campeonato.nombre if instance.campeonato is not None else '',
            'fecha':instance.fecha,
            'equipo_local':instance.equipo_local.nombre if instance.equipo_local is not None else '',
            'equipo_visitante':instance.equipo_visitante.nombre if instance.equipo_visitante is not None else '',
            'score':f"{goles_local}-{goles_visitante}"
        }
    



class SancionDetailSerializer(serializers.ModelSerializer):
    equipo_local=EquipoSerializer(many=True,read_only=True)
    equipo_visitante=EquipoSerializer(many=True,read_only=True)
    jugador=JugadorSerializer(many=True,read_only=True)
    class Meta:
        model=Encuentro
        exclude=['state','deleted_date','modified_date']

    def to_representation(self, instance):

        
        equipo_local_representation={
            'id': instance.equipo_local.id,
            'nombre': instance.equipo_local.nombre,
            'delegado': instance.equipo_local.delegado,  # Ajusta según la lógica de tu aplicación
        }
        equipo_visitante_representation={
            'id': instance.equipo_visitante.id,
            'nombre': instance.equipo_visitante.nombre,
            'delegado': instance.equipo_visitante.delegado,  # Ajusta según la lógica de tu aplicación
        }

        sanciones_representation=[{
                'jugador':{
                    'id':sancion.jugador.id,
                    'nombre':sancion.jugador.nombre,
                    'posicion_jugador':sancion.jugador.posicion_jugador,
                    'equipo':sancion.jugador.equipo.nombre,
                },
                
                'tipo':sancion.tipo,
                'minuto':sancion.minuto,
                'motivo':sancion.motivo
            }
            for sancion in instance.sanciones.all()
        ]

        return {
            'id':instance.id,
            'fecha':instance.fecha,
            'campeonato':instance.campeonato.nombre,
            'teams':[
                equipo_local_representation,
                equipo_visitante_representation
            ],
            'sanciones':sanciones_representation
        }




class EncuentroDetailSerializer(serializers.ModelSerializer):
    equipo_local=EquipoSerializer(many=True,read_only=True)
    equipo_visitante=EquipoSerializer(many=True,read_only=True)
    arbitros=ArbitroSerializer(many=True,read_only=True)
    #goles=GolesSerializer(many=True,read_only=True)
    class Meta:
        model=Encuentro
        exclude=['state','deleted_date','modified_date']


    def to_representation(self, instance):

        encuentro_representation={
            'id':instance.id,
            'fecha':instance.fecha,
            'campeonato':instance.campeonato.nombre
        }
        arbitros_representation=[
            {
                'nombre':arbitro.nombre,
                'apellido':arbitro.apellido,
                'tipo':arbitro.tipo,
                'fecha_nacimiento':arbitro.fecha_nacimiento,
                'num_telefono':arbitro.num_telefono
            }
            for arbitro in instance.arbitros.all()
        ]
        equipo_local_representation={
            'id': instance.equipo_local.id,
            'nombre': instance.equipo_local.nombre,
            'delegado': instance.equipo_local.delegado,  # Ajusta según la lógica de tu aplicación
            'foto_delegado': instance.equipo_local.foto_delegado.url if instance.equipo_local.foto_delegado != '' and instance.equipo_local.foto_delegado else '',  # Ajusta según la lógica de tu aplicación
            'logo_equipo':instance.equipo_local.logo_equipo.url if instance.equipo_local.logo_equipo !='' else '', 
        }
        equipo_visitante_representation={
            'id': instance.equipo_visitante.id,
            'nombre': instance.equipo_visitante.nombre,
            'delegado': instance.equipo_visitante.delegado,  # Ajusta según la lógica de tu aplicación
            'foto_delegado': instance.equipo_visitante.foto_delegado.url if instance.equipo_visitante.foto_delegado != '' and instance.equipo_visitante.foto_delegado else '',  # Ajusta según la lógica de tu aplicación
            'logo_equipo':instance.equipo_visitante.logo_equipo.url if instance.equipo_visitante.logo_equipo !='' else '', 
        }
        
        goles_local=instance.goles.filter(jugador__equipo=instance.equipo_local).count()
        goles_visitante=instance.goles.filter(jugador__equipo=instance.equipo_visitante).count()
        sanciones_count=instance.sanciones.count()

        return {
            'encuentro': encuentro_representation,
            'equipos': [
                equipo_local_representation,
                equipo_visitante_representation
            ],
            'score':f'{goles_local}-{goles_visitante}',
            'arbitros':arbitros_representation,
            'sanciones':sanciones_count
        }

