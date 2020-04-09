from django.test import TestCase
from django.urls import reverse, resolve, path, include
from .views import PostViewSet, CommentViewSet
from .models import Post, Comment
from users.models import User
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase, force_authenticate, APIClient

class PostsTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        urlpatters = [
            path('api/', include('posts.urls')),
        ]

    def test_posts_list_get(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
