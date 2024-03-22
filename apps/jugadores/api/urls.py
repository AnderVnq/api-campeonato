from apps.jugadores.api.views import JugadoresApiView
from rest_framework.routers import DefaultRouter



router=DefaultRouter()

router.register('',JugadoresApiView,basename='jugadores')

urlpatterns = router.urls
