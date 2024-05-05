from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView 
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import check_password
from datetime import datetime
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from apps.campeonatos.api.serializer import CustomTokenSerializer
from apps.users.api.serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from firebase_admin import auth
from email_validator import validate_email,EmailNotValidError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.users.models import User





#asdasdasdads rama dev




def is_valid_email(email):
    try:
        v = validate_email(email)
        return True
    except EmailNotValidError as e:
        return False


class FirebaseRegisterView(GenericAPIView):
    permission_classes=[]
    user_serializer=UserSerializer
    token_custom=CustomTokenSerializer



    @swagger_auto_schema(
        request_body=openapi.Schema(
            title='Token Google',
            type=openapi.TYPE_OBJECT,
            required=['token'],
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            status.HTTP_200_OK:openapi.Response(
                None,
                schema=openapi.Schema(
                    title='message register',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message':openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='message register ok'
                        )
                    }
                )
            )
        }
    )
    def post (self,request):
        #
        #print(default_app.name)
        print(request)
        try:
            idtoken=request.data.get('idToken')
            decode_token=auth.verify_id_token(idtoken,clock_skew_seconds=1)
            print(decode_token)
            name=decode_token['name']
            email=decode_token['email']
            nombre,apellido=name.split(' ')
            #print(nombre,apellido)
            exists=User.objects.filter(username=name,email=email).exists()
            if exists:
                return Response({'message':"Usuario ya está registrado"},status=status.HTTP_400_BAD_REQUEST)
            else:
                contraseña_generada=nombre+"123"  #User.objects.make_random_password() podemos hacer eso o jalar solo el uid y asi lo ponemos de contra
                print('contrasela generada',contraseña_generada)
                hash_password=make_password(contraseña_generada)
                print(hash_password)
                user=User.objects.create(
                    username=name,
                    email=email,
                    password=hash_password
                )
                user.save()
                user_serializer=UserSerializer(user)
                return Response({'message': 'Usuario registrado correctamente','data':user_serializer.data}, status=status.HTTP_201_CREATED)
        except auth.InvalidIdTokenError:
            return Response({'error': 'Token de Firebase inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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




    @swagger_auto_schema(
        request_body=openapi.Schema(
            title='Obtain-token',
            type=openapi.TYPE_OBJECT,
            required=['username','password'],
            properties={
                'username':openapi.Schema(type=openapi.TYPE_STRING,title='username'),
                'password':openapi.Schema(type=openapi.TYPE_STRING,title='password'),
            }
        ),
        responses={
            status.HTTP_200_OK:openapi.Response(
                None,
                schema=openapi.Schema(
                    title='PasswordChange',
                    
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token':openapi.Schema(type=openapi.TYPE_STRING,title='token'),
                        'refresh-token':openapi.Schema(type=openapi.TYPE_STRING,title='refresh-token'),
                        'user':openapi.Schema(type=openapi.TYPE_STRING,title='user'),
                        'message':openapi.Schema(type=openapi.TYPE_STRING)
                    },
                    
                )                  
            )
        }

    )
    def post(self, request, *args, **kwargs):
        username_or_email= request.data.get('username','')
        password=request.data.get('password','')
        print(username_or_email)
        print(password)
        if is_valid_email(username_or_email):
            user=authenticate(
                email=username_or_email,
                password=password     
            )
        else:
            user=authenticate(
                username=username_or_email,
                password=password
            )

        if user and check_password(password,user.password):
            login_serializer=self.serializer_class(data=request.data)
            print(login_serializer)
            print("serializer login")
            if login_serializer.is_valid():
                user_serializer=UserSerializer(user)
                created_datetime=datetime.fromtimestamp(login_serializer.validated_data.get('created'))
                expires_datetime=datetime.fromtimestamp(login_serializer.validated_data.get('expires'))
                return Response({
                    'token':login_serializer.validated_data.get('access'),
                    'refresh-token':login_serializer.validated_data.get('refresh'),
                    'created_at': created_datetime,
                    'expires_at':expires_datetime,
                    'user':user_serializer.data,
                    'message':"inicio de session exitoso"
                },status=status.HTTP_200_OK)
            return Response({
                'error':" error al iniciar session"
            },status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error':"contraseña o username incorrecto"
        },status=status.HTTP_400_BAD_REQUEST)



class LoginWhitGoogle(GenericAPIView):
    permission_classes=[]
    serializer_class=CustomTokenSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            title='Login-Google',
            type=openapi.TYPE_OBJECT,
            required='acces-token-google',
            properties={
                'token-google':openapi.Schema(type=openapi.TYPE_STRING,description='Google-token')
            }
        ),
        responses={
            status.HTTP_200_OK:openapi.Response(
                None,
                schema=openapi.Schema(
                    title='PasswordChange',
                    
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message':openapi.Schema(type=openapi.TYPE_STRING,description='Login access sucesfully',)
                    },
                    
                )                  
            )
        }

    )
    def post(self,request,*args, **kwargs):

        id_token=request.data.get('idToken','')
        try:
            decode_token=auth.verify_id_token(id_token)
            print(decode_token)
            name=decode_token['name']
            username=name.replace(' ','')
            email=decode_token['email']
            contraseña=decode_token['uid']
            print(name,email)
            print(username)
            print("hola")

            #user=User.objects.filter(username=username,email=email)
            user=authenticate(
                username=username,
                password=contraseña
               
            )
            print(user)
            if user:
                #user_serializer=UserSerializer(user)
                login_serializer= self.serializer_class(data={'username':username,'password':contraseña})
                print(login_serializer)
                if login_serializer.is_valid():
                    user_serializer=UserSerializer(user)
                    #login(request,user)
                    return Response({
                        'token':login_serializer.validated_data.get('access'),
                        'refresh-token':login_serializer.validated_data.get('refresh'),
                        'user':user_serializer.data,
                        'message':"inicio de session exitoso"
                    },status=status.HTTP_200_OK)
            else:
                return Response({
                    'message':"Usuario no registrado"
                },status=status.HTTP_400_BAD_REQUEST)
        except auth.InvalidIdTokenError:
            return Response({'error': 'Token de Firebase inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Logout(GenericAPIView):
    permission_classes=[]

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
            else:
                return Response({
                    'message':"session no iniciada"
                })
        return Response({
            'error':"error al cerrar session , no existe usuario"
        },status=status.HTTP_400_BAD_REQUEST)



class CustomObatintokenView(TokenObtainPairView):
    


    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK:openapi.Response(
                None,
                schema=openapi.Schema(
                    title='Obtain token',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access':openapi.Schema(type=openapi.TYPE_STRING,description='access-token'),
                        'refresh':openapi.Schema(type=openapi.TYPE_STRING,description='resfresh-token')
                    }
                )
            )
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)



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
        