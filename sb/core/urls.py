from django.urls import URLPattern, path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    path("settings", views.settings, name="settings"),
    path("upload", views.upload, name="upload"),

    path("like-post",  views.like_post, name="like-post"),
    path("profile/<str:pk>",  views.profile, name="abc"),

    path("follow",  views.follow, name="follow"),
    path("search",  views.search, name="search"),
    # api comment
    path("comment-post",  views.commentPost, name="comment-post"),
    path("comment-post/<str:pk>",  views.commentPostRUD, name="comment-post"),
    # api comment
    path("post/<str:pk>/comments",  views.getPostComments, name="post-comments")



]
