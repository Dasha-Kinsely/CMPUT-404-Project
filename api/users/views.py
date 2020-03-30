from django.shortcuts import render
from rest_framework import viewsets, generics, mixins

from users.models import User
from users.serializers import UserSerializer


# code reference:
# Andreas Poyiatzis; https://medium.com/@apogiatzis/create-a-restful-api-with-users-and-jwt-authentication-using-django-1-11-drf-part-2-eb6fdcf71f45
class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    '''
    retrieve:
        Return a user instance.

    list:
        Return all users,ordered by ID.

    delete:
        Remove a existing user.

    partial_update:
        Update one or more fields on a existing user.

    update:
        Update a user.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer