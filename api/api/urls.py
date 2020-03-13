from django.contrib import admin
import uuid
from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter(trailing_slash=True)


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include([
        path('', include('users.urls')),
        path('', include('posts.urls')),
        path('', include('friendships.urls'))]
    )),
    #path('api/comments', include('comments.urls')),
    #path('api/friendships/', include('friendships.urls')),
    #path('api-auth/', include('rest_framework.urls')),
]