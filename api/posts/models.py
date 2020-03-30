from django.db import models

# Create your models here.
import uuid
from django.utils import timezone
from users.models import User

from config.settings import DEFAULT_HOST

VISIBILITY_CHOICES = [("PUBLIC", "PUBLIC"), 
                      ("FOAF", "FOAF"),
                      ("FRIENDS", "FRIENDS"), 
                      ("PRIVATE", "PRIVATE"), 
                      ("SERVERONLY", "SERVERONLY"), ]
TEXT_TYPE_CHOICES = [("text/plain", "text/plain"),
                     ("text/markdown", "text/markdown"),
                     ("application/base64", "application/base64"),
                     ("image/png;base64", "image/png;base64"),
                     ("image/jpeg;base64", "image/jpeg;base64"),]

class Post(models.Model):
    title = models.CharField(blank=False, max_length=200)
    source = models.URLField(null=False, blank=True)
    origin = models.URLField(null=False, blank=True)
    description = models.TextField(blank=True)
    contentType = models.TextField(choices=TEXT_TYPE_CHOICES, default='text/plain')
    content = models.TextField(blank=True, max_length=2000)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name="post_author")
    categories = models.TextField(default="[]")
    # count = models.IntegerField(default=0)
    size = models.IntegerField(default=50)
    next = models.URLField(null=False, blank=True)
    # comments = models.TextField(default="[]")       #
    published = models.DateTimeField(auto_now_add = True)            # time of the post created
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visibility = models.TextField(choices=VISIBILITY_CHOICES, default='PUBLIC')
    visibleTo = models.TextField(default="[]")
    unlisted = models.BooleanField(default=False)

class Comment(models.Model):
    # post = models.ForeignKey(Post, on_delete = models.CASCADE, default=1, related_name="post_comment")
    post = models.TextField(blank=False, default=1)
    author = author = models.ForeignKey(User, on_delete = models.CASCADE, related_name="comment_author")
    comment = models.TextField(blank=True, max_length=2000)
    contentType = models.TextField(choices=TEXT_TYPE_CHOICES, default='text/plain')
    published = models.DateTimeField(auto_now_add = True)            # time of the comment created
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)