from rest_framework import serializers
from apps.arbitros.models import Arbitro



class ArbitroSerializer(serializers.ModelSerializer):
    class Meta:
        model=Arbitro
        exclude=['state','created_date','modified_date','deleted_date']

    def to_representation(self, instance):
        return {
            'nombre':instance.nombre,
            'apellido':instance.apellido,
            'fecha_nacimiento':instance.fecha_nacimiento,
            'num_telefono':instance.num_telefono,
            'tipo':instance.tipo
        }



class ArbitroListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Arbitro

    def to_representation(self, instance):
        return {
            'nombre':instance['nombre'],
            'apellido':instance['apellido'],
            'fecha_nacimiento':instance['fecha_nacimiento'],
            'num_telefono':instance['num_telefono'],
            'tipo':instance['tipo']
        }



