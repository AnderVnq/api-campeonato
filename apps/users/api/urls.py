from rest_framework.routers import DefaultRouter
from apps.users.api.views import UserViewset



router=DefaultRouter()

router.register('',UserViewset,basename='users')

urlpatterns = router.urls
