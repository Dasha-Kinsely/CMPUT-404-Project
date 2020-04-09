from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, mixins, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
import requests, json

from hosts.models import Host
from hosts.serializers import HostSerializer
from hosts.permissions import IsAdminOrReadOnly

class HostViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        Return a remote host instance.

        Permission:
            Any users: read only

    list:
        Return all remote hosts.
        
        Permission:
            Any users: read only

    delete:
        Remove a existing remote host.

        Permission:
            Admin: delete permission
            Other users: denied

    create:
        Add a new remote host.

        Permission:
            Admin: write permission
            Other users: read only permission
        If the request user is unauthorized or has no permission, a status code "403 Forbidden" will be returned.

        Expected POST request body formmat:
        {
            "baseURL: "https://spongebook-develop.herokuapp.com/",
            "username": "yuan@email.com",
            "password": "passqwer"
        }
        The baseURL should be the common part for APIs, and end with "/".
        Example: "https://cmput-404-project.herokuapp.com/api/"

    partial_update:
        Update one or more fields on a existing host.

        Permission:
            Admin: write permission
            Other users: read only permission
        If the request user is unauthorized or has no permission, a status code "403 Forbidden" will be returned.

    update:
        Update a host.

        Permission:
            Admin: write permission
            Other users: read only permission
        If the request user is unauthorized or has no permission, a status code "403 Forbidden" will be returned.
    '''

    queryset = Host.objects.all()
    serializer_class = HostSerializer
    permission_classes = (IsAdminOrReadOnly,)