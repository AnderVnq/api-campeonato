from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,MultiPartParser
from apps.arbitros.api.serializer import ArbitroSerializer,ArbitroListSerializer
from apps.arbitros.models import Arbitro





class ArbitroApiView(viewsets.GenericViewSet):
    model= Arbitro
    serializer_class = ArbitroSerializer
    list_serializer_class = ArbitroListSerializer



    def get_object(self,pk):
        return get_object_or_404(self.model,pk=pk)
    
    def get_queryset(self):
        if self.queryset is None:
            self.queryset=self.model.objects.filter(state=True).values('id','nombre','apellido','fecha_nacimiento','num_telefono','tipo')
        return self.queryset 
    

    def list(self,request):
        arbitros=self.get_queryset()
        arbitros_serializer=self.list_serializer_class(arbitros,many=True)
        return Response(arbitros_serializer.data,status=status.HTTP_200_OK)
    

    def create(self , request):
        arbitro_serializer=self.serializer_class(data=request.data)
        if arbitro_serializer.is_valid():
            arbitro_serializer.save()
            return Response({
                'message':"Arbitro registrado correctamente",
                'data':arbitro_serializer.data
            },status=status.HTTP_201_CREATED)
        
        return Response({
            'message':"error al registrar Arbitro",
            'error':arbitro_serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    

    def update(self,request,pk=None):
        arbitro=self.get_object(pk)
        arbitro_serializer=self.serializer_class(arbitro,request.data)
        if arbitro_serializer.is_valid():
            arbitro_serializer.save()

            return Response({
                'message':"Arbitro modificado correctamente",
                'data':arbitro_serializer.data
            })
        return Response({
            "message":"Error al actualizar informacion",
            'errors':arbitro_serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    


    def retrieve(self,request,pk=None):
        arbitro=self.get_object(pk)
        arbitro_serializer=self.serializer_class(arbitro)
        return Response(arbitro_serializer.data)
    

    def destroy(self,request,pk):
        arbitro=self.get_object(pk)
        arbitro.state=False
        arbitro.save()
        return Response({
            'message':"arbitro eliminado correctamente"
        })