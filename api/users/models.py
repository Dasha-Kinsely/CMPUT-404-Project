from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from config.settings import DEFAULT_HOST

USER_TYPE_CHOICES = [("author", "Author"), 
                     ("admin", "Admin"),
                     ("host", "Host"),]

# see more: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField(default=DEFAULT_HOST)
    userType = models.TextField(choices=USER_TYPE_CHOICES, default='author', max_length=10)
    # displayName = models.CharField(max_length=20)
    approved = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='uploads', blank=True)
    github = models.URLField(null=False, blank=True) # author github address
    bio = models.TextField(blank=True)