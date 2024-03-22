from rest_framework.routers import DefaultRouter 
from apps.arbitros.api.views import ArbitroApiView



router=DefaultRouter()

router.register('',ArbitroApiView,basename="arbitros")

urlpatterns = router.urls

