from django.urls import re_path,path,include
from django.views.static import serve
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from apps.base.views import Login,Logout              

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion API",
      default_version='v1',
      description="Documentacion API campeonatos futbol",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   re_path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path('users/',include('apps.users.api.urls')),
   path('campeonatos/',include('apps.campeonatos.api.urls')),
   path('encuentros/',include('apps.encuentros.api.urls')),
   path('equipos/',include('apps.equipos.api.urls')),
   path("jugadores/", include('apps.jugadores.api.urls')),
   path("arbitros/", include('apps.arbitros.api.urls')),
   path('login/',Login.as_view(),name='login'),
   path('logout/',Logout.as_view(),name="logout"),
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   #path('refresh-token/',UserToken.as_view(),name='refresh token')
    
]


urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    })
]