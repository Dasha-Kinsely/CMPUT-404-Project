from rest_framework import serializers, exceptions
from rest_auth.serializers import LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer

from allauth.account import adapter, utils

from config import settings
from users.models import User, Host

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

class AuthorRegisterSerializer(RegisterSerializer):

    def return_validated_data(self, arg1, arg2):
        return self.validated_data.get(arg1, arg2)

    def get_data(self):
        return {
            'username': self.return_validated_data('username', ''),
            'password': self.return_validated_data('password', ''),
            'email': self.return_validated_data('email', ''),
            'github': self.return_validated_data('github', ''),
            'userType': 'author',
            'approved': False
        }

    def save_data(self, request):
        author_adapter = adapter.get_adaptor()
        new_author = author_adapter.new_user(request)

        current_host = settings.DEFAULT_HOST
        if Host.objects.filter(url=current_host):
            author_host = Host.object.get(url=current_host)
        else:
            author_host = Host.object.create(url=current_host)
        new_author.host = author_host

        self.cleaned_data = self.get_data()
        author_adapter.save_user(request, new_author, self)
        utils.setup_user_email(request, new_author, self)

        return new_author
