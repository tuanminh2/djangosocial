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
    path("post/<str:pk>/comments",  views.getPostComments, name="post-comments"),

    path("follow/<str:userNameToFollow>",
         views.ajaxFollow, name="ajax-follow"),

    # 404 page
    # page not found
    path("p404",  views.p404, name="p404"),
    # 500
    # server err
    path("p500",  views.p500, name="p500"),
    path("gmore",  views.getMorePost, name="gmore"),





]
