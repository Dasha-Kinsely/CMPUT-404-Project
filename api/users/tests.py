from django.test import TestCase
from django.urls import reverse, resolve, path, include
from .views import LogInAPIView, CurrentAPIView, UserViewSet
from .models import User
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase, force_authenticate, APIClient
from django.contrib.auth import get_user_model
from knox.models import AuthToken

class UsersTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        urlpatters = [
            path('api/', include('users.urls')),
        ]

    def test_authors_list_get(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_login_logout_response(self):
        client = APIClient()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        url = reverse('login')
        responseGET = self.client.get(url)
        self.assertEqual(responseGET.status_code, 405)
        responsePOST = self.client.post(url, {"username":"temporary", "password":"temporary"})
        self.assertEqual(responsePOST.status_code, 200)
        url = reverse('current_user')
        responsePOST =  self.client.post(url, {"username":"temporary", "password":"temporary"})
        client.force_authenticate(user=user, token = AuthToken.objects.create(user)[1])
        self.assertEqual(responsePOST.status_code, 200)
        url = reverse('knox_logout')
        resposePOST = self.client.post(url, {"username":"temporary", "password":"temporary"})
        self.assertEqual(responsePOST.status_code, 200)
