from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, Contact, Comment
from itertools import chain
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from sb.decorators import query_debugger
from django.forms.models import model_to_dict


@query_debugger
@login_required(login_url='signin')
def index(request):

    loggedUser = User.objects.get(username=request.user.username)
    loggedUserProfile = loggedUser.profile

    feed = []

# get contactlist
    followingContactList = Contact.objects.filter(
        follower=loggedUserProfile).select_related("following")

    followingProfileSet = set()

    # Get my post
    myPostList = loggedUserProfile.posts.all()
    myAvatarUrl = loggedUserProfile.profileimage.url
    for item in myPostList:
        dto = None
        likedPostUserIds = {
            li.profile.userId for li in LikePost.objects.filter(
                post=item).select_related("profile")}

        if request.user.id in likedPostUserIds:
            dto = {'postContent': item,
                   'postUserName': loggedUserProfile.userName,
                   'postAuthAvatar': myAvatarUrl, 'likeButtonColor': "blue"}
        else:
            dto = {'postContent': item,
                   'postUserName': loggedUserProfile.userName,
                   'postAuthAvatar': myAvatarUrl, 'likeButtonColor': "grey"}
        feed.append(dto)
    # Get my follwing posts
    for followingContactI in followingContactList:

        followingProfile = followingContactI.following
        #
        followingProfileSet.add(followingProfile)
        #
        postListI = followingProfile.posts.all()
        avatar_url = followingProfile.profileimage.url
        postUserName = followingProfile.userName
        if (postListI):
            for item in postListI:
                dto = None

                # likedPostUserIds = {
                #     li.profile.userId for li in item.likes.all()}
                likedPostUserIds = {
                    li.profile.userId for li in LikePost.objects.filter(
                        post=item).select_related("profile")}

                if request.user.id in likedPostUserIds:
                    dto = {'postContent': item,
                           'postUserName': postUserName,
                           'postAuthAvatar': avatar_url, 'likeButtonColor': "blue"}
                else:
                    dto = {'postContent': item,
                           'postUserName': postUserName,
                           'postAuthAvatar': avatar_url, 'likeButtonColor': "grey"}
                feed.append(dto)

    # each item in array to a parameter in chain method
    # feed_list = list(chain(*feed))

    allProfile = Profile.objects.all()
    followingProfileSet.add(request.user.profile)
    sugList = [x for x in list(allProfile) if (
        x not in followingProfileSet)]

    return render(request, "index.html", {'userProfile': loggedUserProfile, 'data': feed, 'sugProfieList': sugList})


@login_required
def settings(request):
    userProfile = Profile.objects.get(user=request.user)
    if (request.method == "POST"):
        image = None
        if request.FILES.get('image') == None:
            image = userProfile.profileimage
        else:
            image = request.FILES.get('image')
        bio = request.POST['bio']
        location = request.POST['location']

        userProfile.profileimage = image
        userProfile.bio = bio
        userProfile.location = location
        userProfile.save()
        return redirect('settings')

    return render(request, 'setting.html', {'userProfile': userProfile})


def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                # savedUser = user.save()
                # new_profile = Profile.objects.create(userId=user.id, userName=username,
                #                                      user=user)

                return redirect("/signin")
        else:
            messages.info(request, "Password not matching")
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Authen failed')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        userName = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        newPost = Post.objects.create(
            image=image, caption=caption, profile=request.user.profile)
        return redirect('/')
    else:
        return redirect('/')


def like_post(request):
    loggedUserProfile = request.user.profile
    # use get() for param
    postId = request.POST['postId']

    currentPost = Post.objects.get(id=postId)
    like_filter = LikePost.objects.filter(
        post=currentPost, profile=loggedUserProfile).first()

    if like_filter == None:
        newLike = LikePost.objects.create(
            post=currentPost, profile=loggedUserProfile)
        currentPost.no_of_likes = currentPost.no_of_likes + 1
        likeCount = currentPost.no_of_likes
        currentPost.save()
        return JsonResponse(status=200, data={'message': 'like success', 'likeCount': likeCount})
    else:
        like_filter.delete()
        currentPost.no_of_likes = currentPost.no_of_likes - 1
        likeCount = currentPost.no_of_likes
        currentPost.save()
        return JsonResponse(status=200, data={'message': 'unlike success', 'likeCount': likeCount})


@query_debugger
@login_required(login_url='signin')
def profile(request, pk):
    loggedUserProfile = request.user.profile
    userProfile = Profile.objects.prefetch_related("posts").get(userName=pk)
    userPosts = userProfile.posts.all()
    userPostsLen = len(userPosts)

    if Contact.objects.filter(follower=loggedUserProfile, following=userProfile).first():
        buttonText = 'Unfollow'
    else:
        buttonText = 'Follow'

    followerCount = len(Contact.objects.filter(follower=userProfile))
    followingCount = len(Contact.objects.filter(following=userProfile))
    context = {

        'userProfile': userProfile,
        'userPosts': userPosts,
        'userPostsLen': userPostsLen,
        'buttonText': buttonText,
        'followerCount': followerCount,
        'followingCount': followingCount,

    }
    return render(request, "profile.html", context)


@login_required(login_url='signin')
def follow(request):
    if request.method == "POST":
        followerUserName = request.POST["follower"]
        follwingUserName = request.POST["userName"]

        followerProfile = Profile.objects.get(userName=followerUserName)
        follwingProfile = Profile.objects.get(userName=follwingUserName)

        oldFollow = Contact.objects.filter(follower=followerProfile,
                                           following=follwingProfile).first()

        if (oldFollow):
            deleteFollow = oldFollow.delete()
            return redirect("/profile/"+follwingUserName)
        else:

            newFollow = Contact.objects.create(
                follower=followerProfile, following=follwingProfile)

            return redirect("/profile/"+follwingUserName)

    else:
        return redirect("/")


def search(request):
    userObject = User.objects.get(username=request.user.username)

    if request.method == "POST":
        username = request.POST['nameOfUser']
        username_object = User.objects.filter(username__icontains=username)
        ids = []
        profiles = []
        for useri in username_object:
            ids.append(useri.id)
        for idi in ids:
            profile = Profile.objects.filter(userId=idi).first()
            profiles.append(profile)
        return render(request, 'search.html', {'data': profiles})

    return render(request, 'search.html')


def commentPost(request):

    content = request.POST["content"]
    # use get() for param
    postId = request.POST["postId"]
    print("---------------sfksafmskdmf", postId)
    currentPost = Post.objects.get(id=postId)
    loggedUserProfile = request.user.profile
    newComment = Comment.objects.create(
        post=currentPost, content=content, profile=loggedUserProfile)
    currentPost.no_of_comments = currentPost.no_of_comments + 1
    currentPost.save()
    return JsonResponse(status=200, data={"item": model_to_dict(newComment), "authUserName": loggedUserProfile.userName, "authImg": loggedUserProfile.profileimage.url})


def commentPostRUD(request, pk):
    if request.method == "POST":
        # update and delete
        content = request.POST.get('content')
        oldComment = Comment.objects.get(id=pk)
        if content:
            # update
            oldComment.content = content
            oldComment.save()
            return JsonResponse(status=200, data={"message": "update success"})
        else:
            # delete
            oldComment.delete()
            return JsonResponse(status=200, data={"message": "delete success"})
    return redirect("/")


@query_debugger
def getPostComments(request, pk):

    # use get() for param

    commentsWithProfile = Comment.objects.filter(
        post=pk).select_related("profile")
    data = []
    loggedUserProfile = request.user.profile
    for item in commentsWithProfile:
        if item.profile == loggedUserProfile:
            data.append({"item": model_to_dict(item), "authUserName": item.profile.userName,
                         "authImg": item.profile.profileimage.url, "optionHTML": "<div class='dropdown'> <i role='button' class ='fa fa-ellipsis-h' type='button' data-toggle='dropdown' aria-expanded='false'> </i> <div class ='dropdown-menu'><span class='dropdown-item editCommentBtn'> Edit comment </span> <span class='dropdown-item deleteCommentBtn'> Delete comment <span></div> </div>"})
        else:
            data.append({"item": model_to_dict(item), "authUserName": item.profile.userName,
                         "authImg": item.profile.profileimage.url, "optionHTML": ""})
    # return JsonResponse(status=200, data={'comments': list(comments.values())}, safe=False)

    return JsonResponse(data, safe=False)
