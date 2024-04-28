from rest_framework import serializers
from apps.users.models import User





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        #fields=['id', 'username', 'email','first_name', 'last_name', 'date_joined','last_login','image']
        #exclude=['date_joined','state','created_date','modified_date','deleted_date']


    def to_representation(self, instance:User):
        return {
            'id':instance.id,
            'username':instance.username,
            'email':instance.email,
            'first_name':instance.first_name,
            'last_name':instance.last_name,
            'date_joined':instance.date_joined,
            'last_login':instance.last_login,
            'image':instance.image.url if instance.image !='' and instance.image else '',
            'date_joined':instance.date_joined
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
            'image':instance['image'],
            'date_joined':instance['date_joined']
        }
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','image']




class UserPostSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    email=serializers.CharField()
    class Meta:
        model=User
        fields=['username','password','first_name','last_name','email','image']

    def validate(self, data):

        email_user=User.objects.filter(email__icontains=data['email'])
        if email_user.exists():
            raise serializers.ValidationError('el email ya está en uso')
        
        return data



class UserPaswordResetSerializer(serializers.Serializer):

    password=serializers.CharField(max_length=120,min_length=6,write_only=True)
    validate_password=serializers.CharField(max_length=120,min_length=6,write_only=True)
    def validate(self,data):
        print("print de la data en serializer")
        print(data)
        print("data contra")
        request=self.context.get('request')
        usuario:User=request.user
        print("usuario de request",usuario.is_authenticated)
        if data['password']!=data['validate_password']:
            
            raise serializers.ValidationError('debe ingresar contraseñas iguales')
        return data
    



class UserPasswordChangeSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=50,min_length=6,write_only=True)
    new_password=serializers.CharField(max_length=50,min_length=6,write_only=True)
    validate_password=serializers.CharField(max_length=50,min_length=6,write_only=True)

    def validate(self,data):
        request=self.context.get('request')
        usuario:User=request.user

        if request and usuario.is_authenticated:
            if not usuario.check_password(data['password']) :
                raise serializers.ValidationError("contraseña actual incorrecta")

            elif data['new_password']!= data['validate_password']:
                raise serializers.ValidationError("Error la contraseña nueva debe coincidir")     
        else:
            raise serializers.ValidationError("Error usuario no authenticado")
