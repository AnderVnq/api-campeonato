from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from drf_yasg.utils import swagger_auto_schema  
from drf_yasg import openapi
from apps.users.api.serializer import UserListSerializer,UserSerializer,UserPaswordChangeSerializer,UserPostSerializer



class UserViewset(viewsets.GenericViewSet):
    model=User
    serializer_class=UserSerializer
    list_serializer_class=UserListSerializer
    post_serializer_class=UserPostSerializer


    def get_permissions(self):
        if self.request.method=='POST':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]




    def get_object(self,pk):
        return get_object_or_404(self.model,pk=pk)
            

    def get_queryset(self):
        if self.queryset is None:
            self.queryset=self.model.objects.filter(is_active=True).values('id','username','email','first_name','last_name','date_joined')
        
        return self.queryset
    @swagger_auto_schema(
        operation_description="Change password",
        request_body=UserPaswordChangeSerializer,
        responses={
            status.HTTP_200_OK:openapi.Response(
                None,
                schema=openapi.Schema(
                    title='PasswordChange',
                    
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message':openapi.Schema(type=openapi.TYPE_STRING,description='message change password',)
                    },
                    
                )                  
            )
        }
    )
    @action(detail=True,methods=['POST'])
    def set_password(self,request,pk=None):
        user=self.get_object(pk=pk)
        password_serializer=UserPaswordChangeSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({
                'message':"contraseña cambiada correctamente"
            },status=status.HTTP_200_OK)
        return Response({
            'message':"error en la informacion enviada",
            'errors':password_serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)


    def list(self,request):
        users=self.get_queryset()
        user_serializer=self.list_serializer_class(users,many=True)
        return Response(user_serializer.data,status=status.HTTP_200_OK)
    


    @swagger_auto_schema(
        operation_description='create User',
        request_body=post_serializer_class,
        responses={
            '201':UserSerializer
        }
    )   
    #@get_permissions
    def create(self,request):
        user_serializer=self.post_serializer_class(data=request.data)
        if user_serializer.is_valid():
            validated_data = user_serializer.validated_data
            validated_data['password'] = make_password(validated_data['password'])
            # Crear una instancia de usuario con los datos validados
            user = User.objects.create(**validated_data)
            return Response({
                'message':"usuario registrado correctamente",
                'data':user_serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({'message':"errores en el registro",'errors':user_serializer.errors},status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self,request,pk=None):
        user=self.get_object(pk)
        user_serializer=self.serializer_class(user)
        return Response(user_serializer.data)


    def destroy(self,request,pk):
        user=self.get_object(pk)
        user.is_active=False
        user.save()
        return Response({
            'message':"usuario eliminado correctamente"
        },status=status.HTTP_200_OK)

    def update(self,request,pk=None):
        user=self.get_object(pk)
        user_serializer=self.serializer_class(user,request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message':"usuario actualizado correctamente"
            },status=status.HTTP_200_OK)
        return Response({
            'message':"error en la actualizacion",
            'error':user_serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)