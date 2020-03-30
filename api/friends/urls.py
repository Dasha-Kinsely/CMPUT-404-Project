from django.conf.urls import url, include
from rest_framework import routers
from friends.views import FriendRequestView, FriendRequestRejectView, FriendRequestAcceptView, UserFriendListView, UserFriendCheckView, UserFollowerListView, UserFriendRequestView

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^author/(?P<user_id>.+)/friends/$', UserFriendListView.as_view()),
    url(r'^author/(?P<user_id1>.+)/friends/(?P<user_id2>.+)$', UserFriendCheckView.as_view()),
    url(r'^author/(?P<user_id>.+)/followers/$', UserFollowerListView.as_view()),
    url(r'^author/(?P<user_id>.+)/friendrequests/$', UserFriendRequestView.as_view()),
    url(r'^friendrequest/$', FriendRequestView.as_view({'get': 'list', 'post': 'create'})),
    url(r'^friendrequest/(?P<pk>.+)/update$', FriendRequestView.as_view({'put': 'update'})),
    url(r'^friendrequest/(?P<followee_id>.+)/unfollow$', FriendRequestView.as_view({'delete': 'destroy'})),
    url(r'^friendrequest/(?P<follower_id>.+)/reject$', FriendRequestRejectView.as_view()),
    url(r'^friendrequest/(?P<follower_id>.+)/accept$', FriendRequestAcceptView.as_view()),
]