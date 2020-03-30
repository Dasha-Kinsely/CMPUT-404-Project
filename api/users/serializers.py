from rest_framework import serializers, exceptions
from rest_auth.serializers import LoginSerializer
from rest_auth.serializers import UserDetailsSerializer

from users.models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    displayName = serializers.SerializerMethodField(read_only=True)
    firstName = serializers.SerializerMethodField(read_only=True)
    lastName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'host', 'displayName', 'url', 'github', 'firstName', 'lastName', 'email', 'bio')

    def get_id(self, obj):
        return f"{obj.host}author/{obj.id}"

    def get_url(self, obj):
        return f"{obj.host}author/{obj.id}"

    def get_displayName(self,obj):
        return obj.username

    def get_firstName(self,obj):
        return obj.first_name
    
    def get_lastName(self,obj):
        return obj.last_name

class AuthorInfoSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    displayName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'host', 'displayName', 'url', 'github')

    def get_id(self, obj):
        return f"{obj.host}author/{obj.id}"

    def get_url(self, obj):
        return f"{obj.host}author/{obj.id}"

    def get_displayName(self,obj):
        return obj.username