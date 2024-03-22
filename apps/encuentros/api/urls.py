from rest_framework.routers import DefaultRouter
from apps.encuentros.api.views.encuentro_views import EncuentroModelViewSet
# urlpatterns = [
#     path('arbitros/',ArbitroListApiView.as_view()),
#     #path('encuentros/',EncuentroListCreateApiView.as_view()),
#     #path('encuentros/',EncuentroListApiView.as_view()),
#     #path("encuentro/create", EncuentroCreateApiView.as_view(), name=""),
#     path("encuentro/retrieve/<int:pk>", EncuentroRetrieveApiView.as_view(), name=""), 
#     path("encuentro/destroy/<int:pk>", EncuentroDestroyApiView.as_view(), name="")
# ]

router=DefaultRouter()

router.register('',EncuentroModelViewSet , basename="encuentros")
#router.register(r'',basename="arbitros")
#router.register(r'arbitros',ArbitroModelViewSet,basename='arbitros')
urlpatterns = router.urls
