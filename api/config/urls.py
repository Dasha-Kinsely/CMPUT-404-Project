from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from rest_framework import routers, permissions
# drf-yasg - Yet another Swagger generator
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Documentations
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Admin Only
    path('admin/', admin.site.urls),
    # CORS Authentication
    path('auth/', include('rest_auth.urls')),
    path('auth/register', include('rest_auth.registration.urls')),
    path('auth/accounts/', include('allauth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),     # add login option to Browsable API (authentication offered by rest-framework)
    #Actual Paths
    path('api/', include([
        path('', include('users.urls')),
        path('', include('friends.urls')),
        path('', include('posts.urls')),
    ])),
]
