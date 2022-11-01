from django.db import models
from django.forms import PasswordInput

# Create your models here.
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userId = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimage = models.ImageField(
        upload_to="profile_images", default="defaultimg.jpg")
    location = models.CharField(max_length=100,  blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    userName = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    create_at = models.DateTimeField(default=datetime.now())
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.userName


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    userName = models.CharField(max_length=500)

    def __str__(self):
        return self.userName


class FollowersCount(models.Model):
    follower = models.CharField(max_length=500)
    userName = models.CharField(max_length=500)

    def __str__(self):
        return self.userName
