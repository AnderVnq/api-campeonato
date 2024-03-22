from apps.users.api.serializer import UserListSerializer,UserSerializer,UserPaswordChangeSerializer,UserPostSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action


class UserViewset(viewsets.GenericViewSet):
    model=User
    serializer_class=UserSerializer
    list_serializer_class=UserListSerializer
    post_serializer_class=UserPostSerializer

    def get_object(self,pk):
        return get_object_or_404(self.model,pk=pk)
            

    def get_queryset(self):
        if self.queryset is None:
            self.queryset=self.model.objects.filter(is_active=True).values('id','username','email','first_name','last_name')
        
        return self.queryset
    
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
    

    def create(self,request):
        user_serializer=self.post_serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message':"usuario registrado correctamente"
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