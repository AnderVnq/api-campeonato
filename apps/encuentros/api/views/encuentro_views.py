from django.shortcuts import get_object_or_404 , get_list_or_404
from rest_framework import response ,status
from rest_framework import viewsets
from rest_framework.parsers import JSONParser,MultiPartParser
from rest_framework.decorators import action
from apps.encuentros.api.serializers.encuento_serializer import EncuentroSerializer,EncuentroDetailSerializer,SancionDetailSerializer
from apps.encuentros.models import *
from itertools import combinations
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class EncuentroModelViewSet(viewsets.ModelViewSet):
    model=Encuentro
    serializer_class=EncuentroSerializer
    parser_classes=(JSONParser,MultiPartParser)
    def get_queryset(self):
        if self.queryset is None:
            self.queryset=self.model.objects.filter(state=True)
        return self.queryset

    def get_object(self,pk):
        return get_object_or_404(self.model,pk=pk)
    


    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'encuentro': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'fecha': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                            'campeonato': openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    ),
                    'equipos': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'nombre': openapi.Schema(type=openapi.TYPE_STRING),
                                'delegado': openapi.Schema(type=openapi.TYPE_STRING),
                                'foto_delegado': openapi.Schema(type=openapi.TYPE_STRING),
                                'logo_equipo': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    ),
                    'score': openapi.Schema(type=openapi.TYPE_STRING),
                    'arbitros': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'nombre': openapi.Schema(type=openapi.TYPE_STRING),
                                'apellido': openapi.Schema(type=openapi.TYPE_STRING),
                                'tipo': openapi.Schema(type=openapi.TYPE_STRING),
                                'fecha_nacimiento': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                'num_telefono': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    ),
                    'sanciones': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )
        }
    )
    @action(detail=True,methods=['GET'],url_path='detalle-encuentro')
    def detail_encuentro(self,request,pk=None):
        encuentro=self.get_object(pk=pk)
        encuentro_serializer=EncuentroDetailSerializer(encuentro)
        return response.Response(encuentro_serializer.data)



    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'fecha': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    'campeonato': openapi.Schema(type=openapi.TYPE_STRING),
                    'teams': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'nombre': openapi.Schema(type=openapi.TYPE_STRING),
                                'delegado': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    ),
                    'sanciones': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING)
                    )
                }
            ),
        }
    )
    @action(detail=True,methods=['GET'],url_path='sanciones-encuentro')
    def sancion_detail(self,request,pk=None):
        encuentro=self.get_object(pk=pk)
        encuentro_serializer=SancionDetailSerializer(encuentro)
        return response.Response(encuentro_serializer.data)
    




    def list(self,request):

        encuentros_list=[encuentro.id for encuentro in get_list_or_404(Encuentro)]
        print(encuentros_list)
        grupos_iterable=list(combinations(encuentros_list,2))
        print(grupos_iterable)
        encuentro_serializer=self.get_serializer(self.get_queryset(),many=True)

        #print(encuentro_serializer)
        return response.Response(encuentro_serializer.data,status=status.HTTP_200_OK)

    def update(self, request,pk=None):
        if self.get_object().exists():

            if self.get_queryset(pk):
                #encuentro_serializer=self.serializer_class(self.get_queryset(pk),data=request.data)
                encuentro_serializer=self.serializer_class(instance=self.get_object().get(),data=request.data)
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
    
    # def destroy(self, request,pk=None):
    #     if self.get_object().exists():
    #         self.get_object().get().state=False
    #         
    #         return response.Response({'message':"Eliminado Correctamente"},status=status.HTTP_200_OK)
        
    #     return response.Response({'error': f"Encuentro (id:{pk}) no encontrado"},status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request,pk=None):
        encuentro_instance = self.get_object(pk)
        encuentro_serializer = self.serializer_class(encuentro_instance)
        return response.Response(encuentro_serializer.data, status=status.HTTP_200_OK)

    # def update(self, request,pk=None):
    #     if self.get_queryset(pk):
    #         encuentro_serializer=self.serializer_class(self.get_queryset(pk),data=request.data)
    #         if encuentro_serializer.is_valid():
    #             encuentro_serializer.save()
    #             return response.Response(encuentro_serializer.data,status=status.HTTP_200_OK)
    #         return response.Response({'error':"error datos erroneos"},status=status.HTTP_400_BAD_REQUEST)




# class EncuentroListCreateApiView(generics.ListCreateAPIView):
#     serializer_class=EncuentroSerializer

#     def post(self, request):
#         serializer=self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return response.Response({'message':"Encuentro creado correctamente"},status=status.HTTP_201_CREATED)
        
#         return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def get_queryset(self):
#         return self.get_serializer().Meta.model.objects.filter(state=True)



# class EncuentroRetrieveApiView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class=EncuentroSerializer


#     # def put(self,request,pk=None):
#     #     return response.Response({'error':" No se permite valores null"})
#     def put(self, request,pk=None):
#         if self.get_queryset(pk):
#             encuentro_serializer=self.serializer_class(self.get_queryset(pk),data=request.data)
#             if encuentro_serializer.is_valid():
#                 encuentro_serializer.save()
#                 return response.Response(encuentro_serializer.data,status=status.HTTP_200_OK)
#             return response.Response({'error':"error datos erroneos"},status=status.HTTP_400_BAD_REQUEST)

#     def get_queryset(self,pk=None):
#         if pk is None:
#             return self.get_serializer().Meta.model.objects.filter(state=True)
#         return self.get_serializer().Meta.model.objects.filter(id=pk).first()    

#     def delete(self,request,pk=None):
#         encuentro=self.get_queryset().filter(id=pk).first()

#         if encuentro:
#             encuentro.state=False
#             encuentro.save()
#             return response.Response({'message':"Eliminado Correctamente"},status=status.HTTP_200_OK)
        
#         return response.Response({'error': f"Encuentro (id:{pk}) no encontrado"},status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request,pk=None):
#         if self.get_queryset(pk):
#             encuentro_serializer=self.serializer_class(self.get_queryset(pk))
#             return response.Response(encuentro_serializer.data,status=status.HTTP_200_OK)
#         return response.Response({'error':"No existe un encuentro con esos datos "},status=status.HTTP_400_BAD_REQUEST)

# class EncuentroDestroyApiView(generics.DestroyAPIView):
#     serializer_class=EncuentroSerializer

#     def get_queryset(self):
#         return self.get_serializer().Meta.model.objects.filter(state=True)
    

#     def delete(self,request,pk=None):
#         encuentro=self.get_queryset().filter(id=pk).first()

#         if encuentro:
#             encuentro.state=False
#             encuentro.save()
#             return response.Response({'message':"Eliminado Correctamente"},status=status.HTTP_200_OK)
        
#         return response.Response({'error': f"Encuentro (id:{pk}) no encontrado"},status=status.HTTP_400_BAD_REQUEST)
    
