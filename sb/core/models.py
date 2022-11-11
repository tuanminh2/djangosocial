from django.db import models
from django.forms import PasswordInput

# Create your models here.
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userId = models.IntegerField()
    userName = models.CharField(max_length=100, default="usernamedefaut")
    bio = models.TextField(blank=True)
    profileimage = models.ImageField(
        upload_to="profile_images", default="defaultimg.jpg")
    location = models.CharField(max_length=100,  blank=True)

    def __str__(self):
        return self.user.username

# MANY TO ONE > authUser


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None, related_name="posts")

    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    createdAt = models.DateTimeField(default=datetime.now())
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.profile.userName

# MANY TO ONE > Post
# MANY TO ONE > User


class LikePost(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, default=None, related_name="likes")
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None, related_name="likes")

    def __str__(self):
        return self.profile.userName

# N2N Table store many to many of Profile n2n Profile


class Contact(models.Model):
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None, related_name="follower")
    following = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None, related_name="following")

    def __str__(self):
        return self.userName

# MANY TO ONE > Post
# MANY TO ONE > User


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, default=None, related_name="comments")
    content = models.CharField(max_length=500)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None, related_name="comments")

    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.profile.userName
