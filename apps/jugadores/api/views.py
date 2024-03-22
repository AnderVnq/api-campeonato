from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status,filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser,MultiPartParser
from apps.jugadores.api.serializers import JugadorSerializer,JugadorListSerializer
from apps.jugadores.models import Jugadores
from apps.base.views import validate_file



class JugadoresApiView(viewsets.GenericViewSet):
    model=Jugadores
    serializer_class=JugadorSerializer
    list_serializer_class=JugadorListSerializer
    filter_backends = [filters.SearchFilter] 
    search_fields = ['nombre', 'apellidos']
    parser_classes=(JSONParser,MultiPartParser)
   

    def get_object(self,pk):
        return get_object_or_404(self.model,pk=pk)
    

    def get_queryset(self):
        if self.queryset is None:
            self.queryset=self.model.objects.filter(state=True).values('id','nombre','apellidos','fecha_nacimiento','posicion_jugador','imagen_dni','equipo__nombre')
        return self.queryset
    

    def list(self ,request):
        jugadores=self.get_queryset()
        jugadores_serializer=self.list_serializer_class(jugadores,many=True)
        return Response(jugadores_serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request):

        request_copy=validate_file(request.data,'imagen_dni',False)
        jugadores_serializer=self.serializer_class(data=request_copy)
        if  jugadores_serializer.is_valid():
            jugadores_serializer.save()
            return Response({
                'message':"Jugador Registrado con exito",
                'data':jugadores_serializer.data
            },status=status.HTTP_201_CREATED)
        
        return Response({
            'message':'error al registrar equipo',
            'errors':jugadores_serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
        

    def retrieve(self,request,pk=None):
        jugador=self.get_object(pk)
        jugador_serializer=self.serializer_class(jugador)
        return Response(jugador_serializer.data)
    

    def update(self,request,pk=None):
        jugador=self.get_object(pk)
        jugador_serializer=self.serializer_class(jugador,request.data)
        if jugador_serializer.is_valid():
            jugador_serializer.save()
            return Response({
                'message':"jugador actualizado correctamente",
                'data':jugador_serializer.data
            })
        return Response({
            'message':"error al actualizar jugador",
            'errors':jugador_serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk):
        jugador=self.get_object(pk)
        jugador.state=False
        jugador.save()
        return Response({
            'message':"jugador eliminado correctamente"
        })
    
    @action(detail=False, methods=['GET'])
    def search(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        search_query = request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(nombre__icontains=search_query) | queryset.filter(apellidos__icontains=search_query)
        serializer = self.list_serializer_class(queryset, many=True)
        return Response(serializer.data)




