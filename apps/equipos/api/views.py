from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,MultiPartParser
from rest_framework.decorators import action
from apps.equipos.api.serializers import EquipoSerializer,EquiposListSerializer,EquipoJugadoresSerializer
from apps.equipos.models import Equipos
from apps.campeonatos.models import Grupos
import random



def dividir_lista_aleatoria(lista, tamano_subconjunto):
    # Dividir la lista en subconjuntos del tamaño deseado
    subconjuntos = [lista[i:i+tamano_subconjunto] for i in range(0, len(lista), tamano_subconjunto)]
    
    # Si la última lista es más pequeña que el tamaño deseado, combinarla con la anterior
    if len(subconjuntos[-1]) < tamano_subconjunto and len(subconjuntos) > 1:
        subconjuntos[-2].extend(subconjuntos.pop())
    
    return subconjuntos




class EquipoViewSet(viewsets.GenericViewSet):
    model=Equipos
    serializer_class=EquipoSerializer
    list_serializer_class=EquiposListSerializer
    parser_classes=(JSONParser,MultiPartParser)


    def get_object(self,pk):
        return get_object_or_404(self.model,pk=pk)
            

    def get_queryset(self):
        if self.queryset is None:
            self.queryset=self.model.objects.filter(state=True).values('id','nombre','delegado','foto_delegado','logo_equipo','grupos__nombre')
        
        return self.queryset
    


    def list(self,request):

        encuentros_list=[equipo.nombre for equipo in get_list_or_404(Equipos)]
        # #print(encuentros_list)

        # grupo_a=encuentros_list[0:7] 
        # grupo_b=encuentros_list[7:14]
        # grupo_c=encuentros_list[14:21]
        # grupo_d=encuentros_list[21:]
        # print(grupo_a)
        # print(len(grupo_a))
        # print("grupo")
        # print(grupo_b)
        # print(len(grupo_b))
        # print("grupo")
        # print(grupo_c)
        # print(len(grupo_c))
        # print("grupo")
        # print(grupo_d)
        # print(len(grupo_d))
        # print(len(encuentros_list))
        # grupo=[grupo for grupo in combinations(encuentros_list,7)]
        # print(len(grupo))
        # equipos_orden_random=dividir_lista_aleatoria(random.sample(encuentros_list, len(encuentros_list)),7)
        # print(equipos_orden_random)
        # grupos=Grupos.objects.all()
        # print(grupos)
        # for index , sublist in enumerate(equipos_orden_random):
        #     grupo=grupos[index]
        #     print(grupo)
        #     print(sublist)
        #     for nombre_equipo in sublist:
        #         equipo=Equipos.objects.get(nombre=nombre_equipo)
        #         equipo.grupos=grupo
        #         equipo.save()
        #         print(equipo)
        
        # print(len(equipos_orden_random[3]))
        equipos=self.get_queryset()
        equipos_serializer=self.list_serializer_class(equipos,many=True)
        return Response(equipos_serializer.data,status=status.HTTP_200_OK)


    @action(detail=True,methods=['GET'],url_path='jugadores-equipo')
    def View_players_team(self,request,pk=None):
        equipo=self.get_object(pk)
        equipo_serializer=EquipoJugadoresSerializer(equipo)
        return Response(equipo_serializer.data)



    def create(self,request):
        data=request.data
        data['foto_delegado']= None if type(data['foto_delegado'])== str else data['foto_delegado']
        data['logo_equipo']=None  if type(data['logo_equipo'])== str else data['logo_equipo']
        equipo_serializer=self.serializer_class(data=request.data)
        if equipo_serializer.is_valid():
            equipo_serializer.save()
            return Response({
                'message':"Equipo registrado Correctamente",
                'data':equipo_serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            'message':"Error al registrar equipo",
            'error':equipo_serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    

    def update(self,request,pk):
        equipo=self.get_object(pk=pk)
        equipo_serializer=self.serializer_class(equipo,request.data)
        if equipo_serializer.is_valid():
            equipo_serializer.save()
            return Response({
                "message":"actualizado correctamente",
                'data':equipo_serializer.data
            })
        
        return Response({
            "message":"Error al actualizar informacion",
            'errors':equipo_serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self,request,pk=None):

        equipo=self.get_object(pk=pk)
        print(equipo.grupos)
        equipo_serializer=self.serializer_class(equipo)
        return Response(equipo_serializer.data)


    def destroy(self,request,pk):
        equipo=self.get_object(pk=pk)
        equipo.state=False
        equipo.save()
        return Response({
            "message":"equipo eliminado correctamente"
        })