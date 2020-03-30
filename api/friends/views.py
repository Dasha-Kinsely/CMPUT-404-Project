from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
import re
import json
from django.db.models import Q
from django.http import Http404, HttpResponseBadRequest
from users.models import User
from friends.models import Friend
from friends.serializers import FriendSerializer, FriendReadOnlySerializer, FriendfollowerSerializer, FriendURLSerializer

from rest_framework.reverse import reverse

def dict_to_json(dict):
    return json.loads(json.dumps(dict))

class FriendRequestView(mixins.CreateModelMixin, 
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    '''
    list:
        Return all friend requests of all users, ordered by friend request ID.

    create:
        Create a friend requests between two users (follow and send friend request).

        If Succeed will return status code 200.
        Status code "400 Bad Request" will be returned, if user field and friend field are same.

        Expected POST request body example (author is follower, friend is followee):

        {
            "query":"friendrequest",
            "author": {
                "id":"https://cmput-404-project.herokuapp.com/author/6fbb1f1f-d793-4e46-af23-776516890033",
                "host":"https://cmput-404-project.herokuapp.com/",
                "displayName":"admin",
                "url":"https://cmput-404-project.herokuapp.com/author/6fbb1f1f-d793-4e46-af23-776516890033"
            },
            "friend": {
                "id":"https://cmput-404-project.herokuapp.com/author/77532446-1d81-4e78-a5f2-9a79b295c776",
                "host":"https://cmput-404-project.herokuapp.com/",
                "displayName":"user1",
                "url":"https://cmput-404-project.herokuapp.com/author/77532446-1d81-4e78-a5f2-9a79b295c776"

            }
        }

    delete:
        Remove a existing friend requests by followee ID (unfollow).

        Update the "mutual" field of the follower's friend requests to False.

    update:
        !! Do NOT use this API in the frontend.
        !! This API is only used for developing and testing.
        !! This API will be DEPRECATED!
        !! Update a friend requests.
    '''

    queryset = Friend.objects.all()
    # serializer_class = FriendReadOnlySerializer

    def get_object(self, pk):
        try:
            return Friend.objects.get(id=pk)
        except Friend.DoesNotExist:
            raise Http404

    def get_serializer_class(self):
        if self.action == 'create':
            return FriendfollowerSerializer
        elif self.action == 'update':
            return FriendSerializer
        return FriendReadOnlySerializer

    # def list(self, request):
    #     queryset = Friend.objects.all()
    #     # serializer = FriendReadOnlySerializer(queryset, many=True, context={'request': request})
    #     serializer = self.get_serializer_class()(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)
    
    def create(self, request):
        follower = request.data["author"]
        followee = request.data["friend"]
        followee_id = re.findall(r"(https?://[-A-Za-z0-9+&@#%?=~_|!:,.;]+/)author/([-A-Za-z0-9]+)/?", followee["id"], re.I)[0][1]
        follower_id = re.findall(r"(https?://[-A-Za-z0-9+&@#%?=~_|!:,.;]+/)author/([-A-Za-z0-9]+)/?", follower["id"], re.I)[0][1]
        request_data = {"followee_id": followee_id, "followee_host": followee["host"], "followee_name": followee["displayName"], "followee_url": followee["url"],
                     "follower_id": follower_id, "follower_host": follower["host"], "follower_name": follower["displayName"], "follower_url": follower["url"],}
        serializer = self.get_serializer_class()(data=request_data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, followee_id):
        # followee_id = self.kwargs['followee_id']
        try:
            target = Friend.objects.get(Q(followee_id=followee_id) & Q(follower_id=request.user.id))
        except Friend.DoesNotExist:
            raise Http404

        if target.mutual:       # if target's mutual is True, set followee's mutual to False
            followee = Friend.objects.get(Q(followee_url=target.follower_url) & Q(follower_url=target.followee_url))
            followee_serializer = FriendSerializer(followee, data={"mutual": False}, partial=True)
            if followee_serializer.is_valid(raise_exception=True):      # have to call is_valid() before excution
                self.perform_update(followee_serializer)

        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FriendRequestRejectView(APIView):
    '''
    Reject the friend request of specified follower by follower ID.

    Update the "not_read" field of the friend requests with the specified ID to False.

    !! Using this action after login! Since this action will use the loged-in user's info as followee.
    '''

    def get_object(self, follower_id, request):
        try:
            return Friend.objects.get(Q(followee_id=request.user.id) & Q(follower_id=follower_id))
        except Friend.DoesNotExist:
            raise Http404
    
    def put(self, request, follower_id):
        # follower_id = self.kwargs['follower_id']
        target = self.get_object(follower_id, request)

        serializer = FriendSerializer(target, data={"not_read": False}, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):      # have to call is_valid() before excution
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestAcceptView(APIView):
    '''
    Accept the friend request of specified follower by follower ID.

    Update the "mutual" field of the friend requests with the specified ID to True.
    Update the "not_read" field of the friend requests with the specified ID to False.

    !! Using this action after login! Since this action will use the loged-in user's info as followee.
    '''

    def get_object(self, follower_id, request):
        try:
            return Friend.objects.get(Q(followee_id=request.user.id) & Q(follower_id=follower_id))
        except Friend.DoesNotExist:
            raise Http404
    
    def put(self, request, follower_id):
        # follower_id = self.kwargs['follower_id']
        target = self.get_object(follower_id, request)

        # add the follower to the user's (followee) friend list
        mutual_data = {"followee_id": target.follower_id, "followee_host": target.follower_host, "followee_name": target.follower_name, "followee_url": target.follower_url, 
                       "follower_id": target.followee_id, "follower_host": target.followee_host, "follower_name": target.followee_name, "follower_url": target.followee_url, "mutual": True, "not_read": False}
        mutual_serializer = FriendSerializer(data=mutual_data)      # create a mutual following
        if mutual_serializer.is_valid(raise_exception=True):        # have to call is_valid() before excution
            mutual_serializer.save()

        serializer = FriendSerializer(target, data={"mutual": True, "not_read": False}, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):      # have to call is_valid() before excution
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFriendListView(APIView):
    '''
    get:
        Return all friends of specified user_id.

        Expected response body example:

        {
            "query": "friends",
            "authors": [
                "https://cmput-404-project.herokuapp.com/author/6fbb1f1f-d793-4e46-af23-776516890033",
                "https://cmput-404-project.herokuapp.com/author/898d4703-f173-4a40-a634-890c74a621c5"
            ]
        }

    post:
        Check whether the authors in the list are friends of specified user.

        Expected POST request body example:

        {
            "query":"friends",
            "author":"https://cmput-404-project.herokuapp.com/author/77532446-1d81-4e78-a5f2-9a79b295c776",
            "authors": [
                "https://cmput-404-project.herokuapp.com/author/77532446-1d81-4e78-a5f2-9a79b295c776",
                "https://cmput-404-project.herokuapp.com/author/898d4703-f173-4a40-a634-890c74a621c5",
                "https://cmput-404-project.herokuapp.com/author/6fbb1f1f-d793-4e46-af23-776516890033"
            ]
        }
    '''
    def get(self, request, user_id):
        # user_id = self.kwargs['user_id']
        friends = Friend.objects.filter(Q(followee_id=user_id) & Q(mutual=True))
        friend_list = []
        for friend in friends:
            friend_list.append(friend.follower_url)

        response = {"query": "friends", "authors": friend_list}
        return Response(dict_to_json(response))

    def post(self, request, user_id):
        # user_id = self.kwargs['user_id']
        author_url = request.data['author']
        friend_urls = request.data["authors"]
        friend_list = []
        for friend_url in friend_urls:
            # parsed = re.findall(r"(https?://[-A-Za-z0-9+&@#%?=~_|!:,.;]+/)author/([-A-Za-z0-9]+)/?", friend_url, re.I)
            # friend_id = parsed[0][1]
            # friend_host = parsed[0][0]

            # num_friend = Friend.objects.filter(Q(followee_id=user_id) & Q(follower_id=friend_id) & Q(follower_host=friend_host) & Q(mutual=True)).count()
            num_friend = Friend.objects.filter(Q(followee_url=author_url) & Q(follower_url=friend_url) & Q(mutual=True)).count()
            if num_friend > 0:
                friend_list.append(friend_url)

        response = {"query": "friends", "author": author_url, "authors": friend_list}
        return Response(dict_to_json(response))

class UserFriendCheckView(APIView):
    '''
    Check if two specified users are friends.

    If there is any user_id not exiting (or on the other host), the returned json may be with a empty authors list.

    Expected response body example:
    ```
    {
        "query": "friends",
        "authors": [
            "https://cmput-404-project.herokuapp.com/author/6fbb1f1f-d793-4e46-af23-776516890033",
            "https://cmput-404-project.herokuapp.com/author/77532446-1d81-4e78-a5f2-9a79b295c776"
        ],
        "friends": true
    }
    ```
    '''
    # TODO: add compatibility for not existing user
    def get(self, request, user_id1, user_id2):
        # user_id1 = self.kwargs['user_id1']
        # user_id2 = self.kwargs['user_id2']
        friends = Friend.objects.filter(Q(followee_id=user_id1) & Q(follower_id=user_id2) & Q(mutual=True))
        num_friend = friends.count()
        friend_list = []
        if num_friend > 0:
            is_friend = True
            for friend in friends:      # this loop should only loop once
                friend_list.append(friend.followee_url)
                friend_list.append(friend.follower_url)
        else:
            is_friend = False
            #  TODO: fetch user urls and append them to friend_list
            user1 = User.objects.get(id=user_id1)
            user2 = User.objects.get(id=user_id2)
            friend_list.append(f"{user1.host}author/{user1.id}")
            friend_list.append(f"{user2.host}author/{user2.id}")


        response = {"query": "friends", "authors": friend_list, "friends": is_friend}
        return Response(dict_to_json(response))


class UserFollowerListView(APIView):
    '''
    Return the list of all followers (havn't been accepted/ rejected or the followee unfollowed them) of specified user_id.

    Expected response body example:
    ```
    {
        "query": "followers",
        "authors": [
            "https://cmput-404-project.herokuapp.com/author/6fbb1f1f-d793-4e46-af23-776516890033",
            "https://cmput-404-project.herokuapp.com/author/77532446-1d81-4e78-a5f2-9a79b295c776",
            "https://cmput-404-project.herokuapp.com/author/898d4703-f173-4a40-a634-890c74a621c5"
        ]
    }
    ```
    '''

    def get(self, request, user_id):
        # user_id = self.kwargs['user_id']
        followers = Friend.objects.filter(Q(followee_id=user_id) & Q(mutual=False))
        follower_list = []
        for follower in followers:
            follower_list.append(follower.follower_url)
        
        response = {"query": "followers", "authors": follower_list}
        return Response(dict_to_json(response))

class UserFriendRequestView(APIView):
    '''
    Return the list all friend requests of specified user_id that haven't been accpeted / rejected.

    Expected response body example:
    ```
    {
        "query": "followers",
        "authors": [
            "https://cmput-404-project.herokuapp.com/author/6fbb1f1f-d793-4e46-af23-776516890033",
            "https://cmput-404-project.herokuapp.com/author/77532446-1d81-4e78-a5f2-9a79b295c776",
            "https://cmput-404-project.herokuapp.com/author/898d4703-f173-4a40-a634-890c74a621c5"
        ]
    }
    ```
    '''

    def get(self, request, user_id):
        # user_id = self.kwargs['user_id']
        friend_requests = Friend.objects.filter(Q(followee_id=user_id) & Q(not_read=True))
        friend_request_list = []
        for friend_request in friend_requests:
            friend_request_list.append(friend_request.follower_url)
        
        response = {"query": "followers", "authors": friend_request_list}
        return Response(dict_to_json(response))