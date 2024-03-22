from rest_framework import viewsets,status
from apps.encuentros.models import Goles
from apps.campeonatos.api.serializer import CampeonatoSerializer,TopGolesSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response 
from rest_framework import response
from rest_framework.decorators import action
from apps.campeonatos.models import Campeonato
class CampeonatoViewSet(viewsets.ModelViewSet):
    #queryset=Campeonato.objects.all()
    model=Campeonato
    serializer_class=CampeonatoSerializer


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
            return response.Response({'message':"Encuentro creado correctamente"},status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request,pk=None):
        if self.get_queryset(pk):
            encuentro_serializer=self.serializer_class(self.get_queryset(pk),data=request.data)
            if encuentro_serializer.is_valid():
                encuentro_serializer.save()
                return response.Response(encuentro_serializer.data,status=status.HTTP_200_OK)
            return response.Response({'error':"error datos erroneos"},status=status.HTTP_400_BAD_REQUEST)


    def destroy(self,request,pk=None):
        encuentro=self.get_queryset().filter(id=pk).first()

        if encuentro:
            encuentro.state=False
            encuentro.save()
            return response.Response({'message':"Eliminado Correctamente"},status=status.HTTP_200_OK)
        
        return response.Response({'error': f"Encuentro (id:{pk}) no encontrado"},status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=['GET'],url_path='top-goles')
    def top_goles(self,request,pk=None):
        campeonato=self.get_object(pk=pk)
        goles_serializer=TopGolesSerializer(campeonato)
        return Response(goles_serializer.data)























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