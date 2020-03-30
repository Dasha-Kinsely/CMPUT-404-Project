from django.shortcuts import render

# Create your views here.
import json
from rest_framework import viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Q, Count
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer, CommentEditSerializer
from posts.permissions import IsAuthorOrReadOnly, PostVisibility

from friends.models import Friend

import sys
sys.path.append("..") 
import connection_helper as helper

def dict_to_json(dict):
    return json.loads(json.dumps(dict))

def check_friend(author_url, user_url):
    # check both sides to avoid any accidence
    num_friends1 = Friend.objects.filter(Q(followee_url=author_url) & Q(follower_url=user_url) & Q(mutual=True)).count()
    num_friends2 = Friend.objects.filter(Q(followee_url=user_url) & Q(follower_url=author_url) & Q(mutual=True)).count()
    num_friends = num_friends1 + num_friends2
    if num_friends > 0:
        return True
    else:
        response = helper.check_friend(author_url, user_url)
        return response

def check_FOAF(author, user):
    visible = check_friend(author, user)

    if not visible:             # if not friend, then check if they are FOAF
        author_friends = Friend.objects.filter(Q(followee=author) & Q(mutual=True))
        user_friends = Friend.objects.filter(Q(followee=user) & Q(mutual=True))

        for author_friend in author_friends:
            for user_friend in user_friends:
                if author_friend.follower == user_friend.follower:
                    return True
    else:
        return False

def get_visible_posts(posts, user):
    user_url = f"{user.host}author/{user.id}"
    user_host = user.host
    visible_posts = []

    for post in post:
        author_url = post["author"]["id"]
        author_host = post["author"]["host"]
        if post["author"]["id"] == user_url:                                        # current user's post
            visible_posts.append(post)
        elif post["visibility"] == "SERVERONLY" and user_host == author_host:       # current user in the same server with the author
            visible_posts.append(post)
        elif post["visibility"] == "PRIVATE" and user_url in post["visibleTo"]:     # current user in the visibleTo list
            visible_posts.append(post)
        elif post["visibility"] == "FRIENDS":                                       # current user is the friend of the author
            friend_status = check_friend(author_url, user_url)
            if friend_status:
                visible_posts.append(post)
        # elif post["visibility"] == "FOAF":                                          # current user is the FOAF of the author
        #     FOAF_status = check_FOAF(author_url, user_url)
        #     if FOAF_status:
        #         visible_posts.append(post)

    return visible_posts


    # exclude_posts = []

    # for post in posts:
    #     if post["author"]["id"] != user_url:
    #         if post.visibility == "PRIVATE":                # not author and the post is private
    #             exclude_posts.append(post.id)
    #         elif post.visibility == "FRIENDS" :             # not author and the post is friends visible
    #             visible = check_friend(post.author, user)
    #             if not visible:
    #                 exclude_posts.append(post.id)
    #         elif post.visibility == "FOAF":              # not author and the post is FOAF visible
    #             visible = check_FOAF(post.author, user)
    #             if not visible:
    #                 exclude_posts.append(post.id)
    #         # elif post.visibility == 5:              # not author and the post is another author visible
    #         #     if post.another_author != user:
    #         #         exclude_posts.append(post.id)
    #         # elif obj.visibility == 6:               # not author and the post is friends on same host visible
    #         #     # TODO: check friendship

    # for exclude_post in exclude_posts:
    #     posts = posts.exclude(id=exclude_post)

    # return posts

def get_public_posts(posts):
    public_posts = []
    for post in posts:
        if post["visibility"] == "PUBLIC":
            public_posts.append(post)
    return public_posts

# code reference:
# Andreas Poyiatzis; https://medium.com/@apogiatzis/create-a-restful-api-with-users-and-jwt-authentication-using-django-1-11-drf-part-2-eb6fdcf71f45
class PostViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        Return a post instance.

        Permission:
            Any users: read only permission with posts shared with them

    list:
        Return all listed public posts.

        Permission:
            Any users: read only permission with posts shared with them

    create:
        Create a new post.

        Permission:
            Any users: write permission

    delete:
        Remove a existing post.

        Permission:
            Author: delete permission
            Other users: denied

    partial_update:
        Update one or more fields on a existing post.

        Permission:
            Author: write permission
            Other users: read only permission

        !! Currently DO NOT SUPPORT updating images of the post.
        !! DO NOT TRY updating images.

    update:
        Update a post.

        Permission:
            Author: write permission
            Other users: read only permission

        !! Currently DO NOT SUPPORT updating images of the post.
        !! DO NOT TRY updating images.
    '''
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly, PostVisibility)
    
    def get_serializer_class(self):
        return PostSerializer

    # associate Post with User
    # see more: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#associating-snippets-with-users
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request):
        queryset = Post.objects.filter(Q(visibility="PUBLIC") & Q(unlisted=False))      # local posts
        serializer = self.get_serializer_class()(queryset, many=True, context={'request': request})

        remote_posts = helper.get_remote_posts("https://spongebook-develop.herokuapp.com/")
        post_list = serializer.data + remote_posts
        public_post_list = get_public_posts(post_list)
        # return Response(serializer.data)
        return Response(public_post_list)

class VisiblePostView(APIView):
    '''
    Return all posts that visible to the currently authenticated user.
    '''

    # see more: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
    # serializer_class = PostSerializer
    # permission_classes = (PostVisibility,)

    def get(self, request):
        if self.request.user.is_anonymous:      # to check if current user is an anonymous user first, since Q query cannot accept anonymous user
            return Post.objects.filter(Q(visibility="PUBLIC") & Q(unlisted=False))
        else:
            queryset = Post.objects.filter(Q(unlisted=False))   # local posts
            serializer = PostSerializer(queryset, many=True, context={'request': request})
            remote_posts = helper.get_remote_posts("https://spongebook-develop.herokuapp.com/")
            post_list = serializer.data + remote_posts
            visible_post_list = get_visible_posts(post_list, request.user)

            return visible_post_list

class VisibleUserPostView(generics.ListAPIView):
    '''
    Return all posts of specified user that visible to the currently authenticated user.
    '''
    
    # see more: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
    serializer_class = PostSerializer
    permission_classes = (PostVisibility,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        if self.request.user.is_anonymous:      # to check if current user is an anonymous user first, since Q query cannot accept anonymous user
            return Post.objects.filter(Q(visibility="PUBLIC") & Q(author=user_id) & Q(unlisted=False))
        else:
            posts = get_visible_posts(Post.objects.filter(Q(author=user_id) & Q(unlisted=False)), self.request.user)
            return posts

class CommentViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        Return a post instance.

        Permission:
            Any users: read only permission with posts shared with them

    list:
        Return all comments of the specified post.

        Permission:
            Any users: read only permission with posts shared with them

    create:
        Create a new comment for the specified post.

        Following fields will be generated automatically:
        post: post UUID that specified as post_id in URL 
        author: current user
        published: current time
        id: auto-generated UUID

        Expected POST request body formmat:
        {
            "comment": "string",
            "contentType": "text/plain",
        }

    delete:
        Remove a existing post.

        Permission:
            Author: delete permission
            Other users: denied

    partial_update:
        Update one or more fields on a existing post.

        Permission:
            Author: write permission
            Other users: read only permission

        !! Currently DO NOT SUPPORT updating images of the post.
        !! DO NOT TRY updating images.

    update:
        Update a post.

        Permission:
            Author: write permission
            Other users: read only permission

        !! Currently DO NOT SUPPORT updating images of the post.
        !! DO NOT TRY updating images.
    '''
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CommentEditSerializer
        # elif self.action == 'update':
        #     return FriendSerializer
        # return PostReadOnlySerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        request.data["post"] = post_id

        ok_response = dict_to_json({"query": "addComment", "success": True, "message": "Comment Added"})
        forbidden_response = dict_to_json({"query": "addComment", "success": False, "message": "Comment not allowed"})

        serializer = self.get_serializer_class()(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(ok_response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        queryset = Comment.objects.filter(Q(post=post_id))
        serializer = self.get_serializer_class()(queryset, many=True, context={'request': request})
        return Response(serializer.data)
