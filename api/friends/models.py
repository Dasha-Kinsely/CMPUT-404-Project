from django.db import models
import uuid
from django.utils import timezone
from users.models import User
from config.settings import DEFAULT_HOST

class Friend(models.Model):
    '''
    A pair of users can only have less than two Friend instaces, since there are only following status:
    One-way follow (followee not yet approved): not_read=True
    One-way follow (followee rejected): not_read=False
    Friend (mutual/two-way following): the followee should also create a Friend instance and mark both instances with mutual=True
    Unfollow: delete the Friend instance and mark the followee's instance with mutual=False

    For creating Friend instance and marking mutual field of the followee, it will be finished automatically by the view.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # followee = models.ForeignKey(User, on_delete = models.CASCADE, related_name='friend_followee')
    # follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name='friend_follower')
    followee_id = models.TextField(blank=False, default=1)     # followee's uuid
    followee_host = models.URLField(default=DEFAULT_HOST)
    followee_name = models.CharField(max_length=100, default="user")
    followee_url = models.URLField(default=DEFAULT_HOST)
    follower_id = models.TextField(blank=False, default=1)     # follower's uuid
    follower_host = models.URLField(default=DEFAULT_HOST)
    follower_name = models.CharField(max_length=100, default="user")
    follower_url = models.URLField(default=DEFAULT_HOST)
    mutual = models.BooleanField(default=False)             # wheater the followee followed back
    not_read = models.BooleanField(default=True)            # wheater the followee read this request