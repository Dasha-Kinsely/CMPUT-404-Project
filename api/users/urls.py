from django.conf.urls import url, include
from rest_framework import routers
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'author', UserViewSet, basename="user")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
]