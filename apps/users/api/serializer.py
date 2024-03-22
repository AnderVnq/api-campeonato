from rest_framework import serializers
from django.contrib.auth.models import User





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        #fields='__all__'
        fields=['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        #exclude=['date_joined','state','created_date','modified_date','deleted_date']


    def to_representation(self, instance):
        return {
            'id':instance.id,
            'username':instance.username,
            'email':instance.email,
            'first_name':instance.first_name,
            'last_name':instance.last_name,
            'date_joined':instance.date_joined,
            # 'last_login':instancelast_login,
            # 'is_active':instanceis_active
        }
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model=User


    def to_representation(self, instance):
        return {
            'id':instance['id'],
            'username':instance['username'],
            'email':instance['email'],
            'first_name':instance['first_name'],
            'last_name':instance['last_name'],
        }
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name']




class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']


class UserPaswordChangeSerializer(serializers.Serializer):

    password=serializers.CharField(max_length=120,min_length=6,write_only=True)
    validate_password=serializers.CharField(max_length=120,min_length=6,write_only=True)
    def validate(self,data):
        print(data)
        if data['password']!=data['validate_password']:
            
            raise serializers.ValidationError('debe ingresar contraseñas iguales')
        return data