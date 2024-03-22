from apps.encuentros.models import *
from rest_framework import serializers


class GolesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Goles
        exclude=['state','deleted_date','modified_date']



class SancionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Sancion
        exclude=['state','deleted_date','modified_date']