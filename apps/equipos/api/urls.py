from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.equipos.api.views import EquipoViewSet





router=DefaultRouter()



router.register('',EquipoViewSet,basename='equipos')

urlpatterns = router.urls