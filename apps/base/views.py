from django.contrib.auth import authenticate
from django.contrib.auth.models import User 
#from rest_framework.authtoken.views import ObtainAuthToken
#from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView 
#from apps.campeonatos.api.serializer import UserTokenSerializer
from django.contrib.sessions.models import Session
from datetime import datetime
#from apps.base.authentication import Authentication
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.campeonatos.api.serializer import CustomTokenSerializer
from apps.users.api.serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.



def validate_file(request,field,update=False):

    request=request.copy()

    if update:
        if type(request[field])== str:
            request.__delitem__(field)
        else:
            if type(request[field])==str:request.__setitem__(field,None)

    return request



class Login(TokenObtainPairView):
    serializer_class=CustomTokenSerializer



    def post(self, request, *args, **kwargs):
        username= request.data.get('username','')
        password=request.data.get('password','')

        user=authenticate(
            username=username,
            password=password
        )
        if user:
            login_serializer=self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer=UserSerializer(user)
                return Response({
                    'token':login_serializer.validated_data.get('access'),
                    'refresh-token':login_serializer.validated_data.get('refresh'),
                    'user':user_serializer.data,
                    'message':"inicio de session exitoso"
                },status=status.HTTP_200_OK)
            return Response({
                'error':"contraseña o username incorrecto"
            },status=status.HTTP_400_BAD_REQUEST)






class Logout(GenericAPIView):
    def post(self,request,*args, **kwargs):
        user=User.objects.filter(id=request.data.get('user',0))
        id_user=user.first()
        if user.exists():
            RefreshToken.for_user(user.first())
            all_session=Session.objects.filter(expire_date__gte=datetime.now(),session_key__contains=id_user.id)
            if all_session.exists():
                all_session.delete()
                return Response({
                    'message':"session cerrada correctamente"
                },status=status.HTTP_200_OK)

        return Response({
            'error':"error al cerrar session , no existe usuario"
        },status=status.HTTP_400_BAD_REQUEST)












#esto es un custom login y logout 
# class UserToken(Authentication,APIView):
#     """
#         validate token
#     """

#     def get(self,request,*args, **kwargs):
#         #username=request.GET.get('username')
#         try:
#             #user_token,_=Token.objects.get_or_create(user=UserTokenSerializer().Meta.model.objects.filter(username=self.user.username).first())
#             user_token,_=Token.objects.get_or_create(user=self.user)
#             user=UserTokenSerializer(self.user)
#             return Response({
#                 'token':user_token.key,
#                 'user':user.data
#             })
#         except:
#             return Response({
#                 'error':"credenciales enviadas incorrectas"
#             },status=status.HTTP_400_BAD_REQUEST)


# class Login(ObtainAuthToken):


#     def post(self,request,*args, **kwargs):

#         login_serializer= self.serializer_class(data=request.data,context={'request':request})
#         if login_serializer.is_valid():
#             user=login_serializer.validated_data['user']

#             if user.is_active:
#                 pass
#                 token,created=Token.objects.get_or_create(user=user)
#                 user_serializer=UserTokenSerializer(user)
#                 if created:
#                     return Response({
#                         'token':token.key,
#                         'user':user_serializer.data,
#                         'message':"inicio de session exitoso"
#                     },status=status.HTTP_200_OK)
#                 else:
#                     all_session=Session.objects.filter(expire_date__gte=datetime.now())
#                     if all_session.exists():
#                         for session in all_session:
#                             session_data=session.get_decoded()
#                             if user.id == int(session_data.get('_auth_user_id')):
#                                 session.delete()
#                     token.delete()
#                     token=Token.objects.create(user=user)
#                     return Response({
#                         'token':token.key,
#                         'user':user_serializer.data,
#                         'message':"inicio de session exitoso"
#                     },status=status.HTTP_200_OK)
#                     #token.delete()
#                     #return Response({'message':"session ya iniciada "}, error 409)
#             else:
#                 return Response({'message':"error usuario no puede iniciar sesion"},status=status.HTTP_401_UNAUTHORIZED)
            
#         else:
#             return Response({'message':"usuario o contraseña incorrecta"},status=status.HTTP_400_BAD_REQUEST)
#         #return Response({'message':"helou"},status=status.HTTP_200_OK)





# class Logout(APIView):


#     def post(self,request,*args, **kwargs):
#         try:
#             token=request.POST.get('token')
#             token=Token.objects.filter(key=token).first()
#             if token:
#                 user=token.user
#                 all_session=Session.objects.filter(expire_date__gte=datetime.now())
#                 if all_session.exists():
#                     for session in all_session:
#                         session_data=session.get_decoded()
#                         if user.id == int(session_data.get('_auth_user_id')):
#                             session.delete()
#                 session_message='Sessiones de usuario eliminado'
#                 token.delete()
#                 token_message="token eliminado"
#                 return Response({
#                     'token_message':token_message,
#                     'session_message':session_message,
#                 },status=status.HTTP_200_OK)
#             return Response({'errors':"no se encontro usuario con estas credenciales"},status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({
#                 'error':"no se encontro token en la peticion"
#             },status=status.HTTP_409_CONFLICT)
        