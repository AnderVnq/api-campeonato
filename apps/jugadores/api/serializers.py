from rest_framework import serializers
from apps.jugadores.models import Jugadores
#from apps.equipos.api.serializers import EquipoSerializer

class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Jugadores
        exclude=['state','created_date','modified_date','deleted_date']


    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'apellidos':instance.apellidos,
            'fecha_nacimiento':instance.fecha_nacimiento,
            'posicion_jugador':instance.posicion_jugador,
            'imagen_dni':instance.imagen_dni.url if instance.imagen_dni!= '' else '',
            'equipo':instance.equipo.nombre
        }


class JugadorListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Jugadores
        exclude=['state','created_date','modified_date','deleted_date']

    

    def to_representation(self, instance):
        return {
            'id':instance['id'],
            'nombre':instance['nombre'],
            'apellidos':instance['apellidos'],
            'fecha_nacimiento':instance['fecha_nacimiento'],
            'posicion_jugador':instance['posicion_jugador'],
            'imagen_dni':instance['imagen_dni'],
            'equipo':instance['equipo__nombre'],
        }
    

# class JugadorEquipoSerializer(serializers.ModelSerializer):
#     equipo=EquipoSerializer()
#     class Meta:
#         model=Jugadores
#         exclude=['state','created_date','modified_date','deleted_date']