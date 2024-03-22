from rest_framework.routers import DefaultRouter
from apps.campeonatos.api.views import CampeonatoViewSet




router=DefaultRouter()

router.register('',CampeonatoViewSet,basename='campeonatos')
urlpatterns = router.urls
