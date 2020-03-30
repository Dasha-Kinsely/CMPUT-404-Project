from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from config.settings import DEFAULT_HOST

USER_TYPE_CHOICES = [("author", "Author"), 
                     ("admin", "Admin"),
                     ("host", "Host"),]

# see more: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model
class User(AbstractUser):
    #URLFields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    github = models.URLField(null=False, blank=True) # author github address
    host = models.URLField(default=DEFAULT_HOST)
    #For admin use only
    approved = models.BooleanField(default=False)
    userType = models.TextField(choices=USER_TYPE_CHOICES, default='author', max_length=10)
    #Image data
    avatar = models.ImageField(upload_to='uploads', blank=True)
    #Details in string datatypes
    bio = models.TextField(blank=True)
    # displayName = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
 

class Host(models.Model):
    url = models.URLField(max_length=400)
    serviceUsername = models.CharField(
        max_length=100, null=True, blank=True)
    servicePassword = models.CharField(
        max_length=100, null=True, blank=True)

