from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives,EmailMessage,send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from drf_yasg.utils import swagger_auto_schema  
from drf_yasg import openapi
from apps.users.api.serializer import UserListSerializer,UserSerializer,UserPaswordResetSerializer,UserPostSerializer,UserPasswordChangeSerializer
from apps.users.models import Historical_Emails,User
import jwt
from datetime import datetime, timedelta
from django.conf import settings


class UserViewset(viewsets.GenericViewSet):
    model=User
    serializer_class=UserSerializer
    list_serializer_class=UserListSerializer
    post_serializer_class=UserPostSerializer
    #permission_classes=[]


    def get_permissions(self):
        if self.action == 'destroy' or self.action=="update":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes=[]
        return [permission() for permission in permission_classes]


    def get_object(self,pk):
        return get_object_or_404(self.model,pk=pk)
            

    def get_queryset(self):
        if self.queryset is None:
            self.queryset=self.model.objects.filter(is_active=True).values('id','username','email','first_name','last_name','date_joined','image')
        
        return self.queryset
    



    @swagger_auto_schema(
        operation_description="Change password",
        request_body=UserPaswordResetSerializer,
        responses={
            status.HTTP_200_OK:openapi.Response(
                None,
                schema=openapi.Schema(
                    title='PasswordChange',
                    
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message':openapi.Schema(type=openapi.TYPE_STRING,description='message reset password',)
                    },
                    
                )                  
            )
        }
    )
    @action(detail=True,methods=['POST'])
    def reset_password(self,request,pk=None):
        user=self.get_object(pk=pk)
        info_usuario=request.user
        print("info usuario:",info_usuario.password)
        print("is aunthenticate",info_usuario.is_authenticated)
        print("request##############")
        print(request.data)
        password_serializer=UserPaswordResetSerializer(data=request.data,context={'request':request})
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['validate_password'])
            user.save()
            #acá se añade eso del email
            return Response({
                'message':"contraseña cambiada correctamente"
            },status=status.HTTP_200_OK)
        return Response({
            'message':"error en la informacion enviada",
            'errors':password_serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)





    @swagger_auto_schema(
        operation_description="Change password",
        request_body=UserPasswordChangeSerializer,
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
    @action(detail=True,methods=['POST'],permission_classes=[IsAuthenticated])
    def user_change_password(self,request,pk=None):
        user=self.get_object(pk=pk)
        password_serializer=UserPasswordChangeSerializer(data=request.data,context={'request':request})
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['validate_password'])
            user.save()
            return Response({
                'message':"Contraseña cambiada correctamente"
            },status=status.HTTP_200_OK)
        else:
           return Response({
            'message':"error en la informacion enviada",
            'errors':password_serializer.errors
           },status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            title='Email-acount',
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING,title='gmail')
            }
        )
    )
    @action(detail=False,methods=['POST'],url_path='email-reset-password')
    def send_solicitud(self,request):
        subject="Reset you password"
        to_email=request.data['email']
        token_payload = {
            'email': to_email,
            'exp': timezone.now()+ timedelta(hours=1)  # Caduca en 1 hora
        }
        token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
            
        reset_link = f"https://example.com/reset-password?token={token}"
        html_message=render_to_string('email_template.html',{'reset_link':reset_link})
        text_content=strip_tags(html_message)
        email=EmailMultiAlternatives(
            subject=subject,
            # message=message,
            # text_content=text_content,
            to=[to_email]
        )
        email.attach_alternative(html_message,"text/html")
        usuarios=User.objects.filter(email=to_email)
        if not usuarios.exists():
            return Response({
                'message': "Ingrese su email correctamente"
            })
        usuario=usuarios.first()
        registro_email=Historical_Emails.objects.create(
            send_to=usuario,
            asunto=subject
        )
        registro_email.save()
        email.send()
        return Response({
            'message':"email enviado correctamente",
            'token':token
        },status=status.HTTP_200_OK)
    #vista para enviar mail de reset password 


    def list(self,request):
        users=self.get_queryset()
        user_serializer=self.list_serializer_class(users,many=True)
        return Response(user_serializer.data,status=status.HTTP_200_OK)
    


    # @swagger_auto_schema(
    #     operation_description='create User',
    #     request_body=post_serializer_class,
    #     responses={
    #         '201':UserSerializer
    #     }
    # )   
    # #@get_permissions
    def create(self,request):
        #self.permission_classes=[]
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
        self.permission_classes=[IsAuthenticated]
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