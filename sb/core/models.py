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
    # Consistency trade-off with user table for high traffic of read side:
    userName = models.CharField(
        max_length=100, default="usernamedefaut", unique=True)
    bio = models.TextField(blank=True)
    profileimage = models.ImageField(
        upload_to="profile_images", default="defaultimg.jpg")
    location = models.CharField(max_length=100,  blank=True)

    # index for searching speed
    indexes = [
        models.Index(fields=['userName', ]),
    ]

    def __str__(self):
        return self.user.username

    # overide save method
    def save(self, *args, **kwargs):

        self.userName = self.user.username
        self.userId = self.user.id

        super().save(*args, **kwargs)


# MANY TO ONE > Profile


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None, related_name="posts")

    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    createdAt = models.DateTimeField(default=datetime.now())
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)

    class Meta:
        ordering = ["-createdAt"]

    def __str__(self):
        return self.profile.userName

# MANY TO ONE > Post
# MANY TO ONE > Profile


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
        Profile, on_delete=models.CASCADE, default=None, related_name="followers")
    following = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None, related_name="followings")

    def __str__(self):
        return self.follower.userName+" to "+self.following.userName

# MANY TO ONE > Post
# MANY TO ONE > Profile


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

    class Meta:
        ordering = ["-createdAt"]
