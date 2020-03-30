from django.conf.urls import url, include
from rest_framework import routers
from posts.views import PostViewSet, VisiblePostView, VisibleUserPostView, CommentViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^author/posts$', VisiblePostView.as_view()),
    url(r'^author/(?P<user_id>.+)/posts$', VisibleUserPostView.as_view()),
    url(r'^posts/(?P<post_id>.+)/comments$', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
]