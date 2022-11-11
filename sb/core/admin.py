from django.contrib import admin
from .models import Profile, Post, LikePost, Contact, Comment
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Contact)
admin.site.register(Comment)
