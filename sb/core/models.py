from django.db import models
from django.forms import PasswordInput

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userId = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimage = models.ImageField(
        upload_to="profile_images", default="defaultimg.jpg")
    location = models.CharField(max_length=100,  blank=True)

    # def __str__(self):
    #     return self.user.username
