from rest_framework import serializers
from apps.equipos.models import Equipos
from apps.jugadores.api.serializers import JugadorSerializer


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Equipos
        exclude=['state','created_date','modified_date','deleted_date']

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'delegado':instance.delegado,
            'foto_delegado': instance.foto_delegado.url if instance.foto_delegado != '' and instance.foto_delegado else '',
            'logo_equipo':instance.logo_equipo.url if instance.logo_equipo !='' and instance.logo_equipo else '',
            'grupo':instance.grupos.nombre if instance.grupos is not None else ''

        }
    
class EquiposListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Equipos


    def to_representation(self, instance):
        return {
            'id':instance['id'],
            'nombre':instance['nombre'],
            'delegado':instance['delegado'],
            'foto_delegado':instance['foto_delegado'],
            'logo_equipo':instance['logo_equipo'],
            'grupo':instance['grupos__nombre'] if instance['grupos__nombre'] !=None and instance['grupos__nombre']!= None else ''
        }
    

class EquipoJugadoresSerializer(serializers.ModelSerializer):
    jugadores=JugadorSerializer(many=True , read_only=True)
    class Meta:
        model=Equipos
        exclude=['state','created_date','modified_date','deleted_date']
    def to_representation(self, instance):
        equipo_representation = {
            'id': instance.id,
            'nombre': instance.nombre,
            'delegado': instance.delegado,  # Ajusta según la lógica de tu aplicación
            'foto_delegado': instance.foto_delegado.url if instance.foto_delegado != '' and instance.foto_delegado else '',  # Ajusta según la lógica de tu aplicación
            'logo_equipo':instance.logo_equipo.url if instance.logo_equipo !='' else '',  # Ajusta según la lógica de tu aplicación
        }
        jugadores_representation = [
            {
                'id': jugador.id,
                'nombre': jugador.nombre,
                'apellidos': jugador.apellidos,
                'fecha_nacimiento': jugador.fecha_nacimiento,
                'posicion_jugador': jugador.posicion_jugador,
                'imagen_dni': jugador.imagen_dni.url if jugador.imagen_dni else '',
                'equipo': instance.nombre,
            }
            for jugador in instance.jugadores.all()
        ]

        return {
            'equipo': equipo_representation,
            'jugadores': jugadores_representation,
        }