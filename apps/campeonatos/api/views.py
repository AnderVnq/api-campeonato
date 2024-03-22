from django.core.mail import send_mail,EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status
from rest_framework.response import Response 
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser,MultiPartParser
from apps.campeonatos.models import Campeonato
from apps.campeonatos.api.serializer import CampeonatoSerializer,TopGolesSerializer

class CampeonatoViewSet(viewsets.ModelViewSet):
    #queryset=Campeonato.objects.all()
    model=Campeonato
    serializer_class=CampeonatoSerializer
    parser_classes=(JSONParser,MultiPartParser)


    def get_object(self,pk):
        return get_object_or_404(self.model,pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset=self.model.objects.filter(state=True)
        return self.queryset
    
    def list(self,request):
        campeonato_serializer=self.get_serializer(self.get_queryset(),many=True)
        return Response(campeonato_serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Encuentro creado correctamente"},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request,pk=None):
        if self.get_queryset(pk):
            encuentro_serializer=self.serializer_class(self.get_queryset(pk),data=request.data)
            if encuentro_serializer.is_valid():
                encuentro_serializer.save()
                return Response(encuentro_serializer.data,status=status.HTTP_200_OK)
            return Response({'error':"error datos erroneos"},status=status.HTTP_400_BAD_REQUEST)


    def destroy(self,request,pk=None):
        encuentro=self.get_queryset().filter(id=pk).first()

        if encuentro:
            encuentro.state=False
            encuentro.save()
            return Response({'message':"Eliminado Correctamente"},status=status.HTTP_200_OK)
        
        return Response({'error': f"Encuentro (id:{pk}) no encontrado"},status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request,pk=None):
        campeonato=self.get_object(pk=pk)
        campeonato_serializer=self.serializer_class(campeonato)
        return Response(campeonato_serializer.data)

    @action(detail=True,methods=['GET'],url_path='top-goles')
    def top_goles(self,request,pk=None):
        campeonato=self.get_object(pk=pk)
        goles_serializer=TopGolesSerializer(campeonato)
        return Response(goles_serializer.data)


    @action(detail=True,methods=['POST'],url_path='send-email-bases')
    def send_view_bases(self,request,pk=None):
        try:
            campeonato=self.get_object(pk=pk)
            to_email='ndrsnvenegas@gmail.com'
            rutas_bases={
                'libre_verano':"media/bases/bases_libre_verano.pdf",
                'libre_invierno':"C:/Users/HP/Desktop/api_camp/media/bases/bases_libre_invierno.pdf",
                'master':"media/bases/bases_libre_verano_master.pdf",
            }
            if 'master' in campeonato.tipo:
                pdf=rutas_bases['master']
            elif 'libre' in campeonato.tipo and 'verano' in campeonato.tipo:
                pdf=rutas_bases['libre_verano']
            else:
                pdf=rutas_bases['libre_invierno']

            email_subject=f'Bienvenido a {campeonato.nombre} '
            email_body=f'El campeonato que se realizará el dia {campeonato.fecha_inicio} - hasta {campeonato.fecha_fin}'
            email=EmailMessage(email_subject,email_body,to=[to_email])
            email.attach_file(pdf)
            email.send()
            return Response({
                'message':"informacion enviada con exito"
            },status=status.HTTP_200_OK)
        except Exception as e:
            error=str(e)
            return Response({
                'message':"Error al enviar informacion",
                'errors':error
            },status=status.HTTP_400_BAD_REQUEST)





















# @api_view(['GET','POST'])
# def users_api_view(request):
#     if request.method=='GET':
#         users=User.objects.all().values('id', 'username', 'email', 'first_name', 'last_name', 'date_joined','last_login','is_active')
#         user_serializer=UserSerializer(users,many=True)
#         return Response(user_serializer.data)
    
#     elif request.method == 'POST':
#         user_serializer=UserSerializer(data=request.data)
#         if user_serializer.is_valid():
#             user_serializer.save()
#             return Response(user_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(user_serializer.errors , status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET','PUT','DELETE'])
# def user_detail_view(request,pk):

#     user=User.objects.filter(id=pk).first()

#     if user:
#         if request.method== 'GET':

#             user_serializer=UserSerializer(user)
#             return Response(user_serializer.data , status=status.HTTP_200_OK)
        
#         elif request.method == 'PUT':

#             user_serializer=UserSerializer(user,data=request.data)
#             if user_serializer.is_valid():
#                 user_serializer.save()
#                 return Response(user_serializer.data,status=status.HTTP_200_OK)
        
#             return Response(user_serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
        
#         elif request.method == 'DELETE':
#             user.delete()
#             return Response({'message':'usuario eliminado correctamente'},status=status.HTTP_200_OK)

#     return Response({'message':'Usuario no encontrado'},status=status.HTTP_400_BAD_REQUEST)