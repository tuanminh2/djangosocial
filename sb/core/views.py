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


@csrf_exempt
def getMorePost(request, page):
    if (request.method == "POST"):

        rs = []

        loggedUser = request.user
        loggedUserProfile = loggedUser.profile
        fid = str(loggedUserProfile.id)
        limit = 5
        offset = (page-1) * limit
        sql = "select pst.id, pst.caption from core_post as pst inner join core_profile as pro on pst.profile_id = pro.id where pro.id in (select ct.following_id from core_contact as ct where ct.follower_id = "+str(
            fid)+") "
        sql = sql + "LIMIT "+str(limit) + " OFFSET "+str(offset)
        next5post = Post.objects.raw(sql)
        print(len(next5post))
        for postItem in next5post:
            likedPostUserIds = {
                li.profile.userId for li in LikePost.objects.filter(
                    post=postItem).select_related("profile")}
            dto = None
            if request.user.id in likedPostUserIds:

                dto = {"postId": postItem.id,
                       "postContent": postItem.caption,
                       "postImg": postItem.image.url,
                       "postUserName": postItem.profile.userName,
                       "postCreatedAt": postItem.createdAt,
                       "postLikeCount": postItem.no_of_likes,
                       "loggedUserAvt": loggedUserProfile.profileimage.url,
                       "loggedUserName": loggedUserProfile.userName,
                       "postAuthAvatar": postItem.profile.profileimage.url, "likeButtonColor": "blue"}
            else:
                dto = {"postId": postItem.id,
                       "postContent": postItem.caption,
                       "postImg": postItem.image.url,
                       "postUserName": postItem.profile.userName,
                       "postCreatedAt": postItem.createdAt,
                       "postLikeCount": postItem.no_of_likes,
                       "loggedUserAvt": loggedUserProfile.profileimage.url,
                       "loggedUserName": loggedUserProfile.userName,
                       "postAuthAvatar": postItem.profile.profileimage.url, "likeButtonColor": "grey"}

            rs.append(dto)

    return JsonResponse(rs, safe=False)


@query_debugger
@login_required(login_url='signin')
def index(request):
    # Use get() for get single one
    loggedUser = User.objects.get(username=request.user.username)
    loggedUserProfile = loggedUser.profile

    feed = []

    # get contactlist
    # select_related store data in query cache
    # Good : use join with select_related instead to reduce number of query
    followingContactList = Contact.objects.filter(
        follower=loggedUserProfile).select_related("following")

    # FOR SUGGESTION
    allProfile = Profile.objects.all()

    # use Set to improve speed when check contain
    followingProfileSet = set()
    followingProfileSet.add(request.user.profile)
    for item in followingContactList:
        followingProfileSet.add(item.following)

    # use Set instead List for check exist to improve speed
    sugList = [x for x in list(allProfile) if (
        x not in followingProfileSet)]
    # FOR SUGGESTION

    # Get my posts
    myPostList = loggedUserProfile.posts.all()
    myAvatarUrl = loggedUserProfile.profileimage.url
    cnt = 0
    for item in myPostList:
        if cnt == 5:
            return render(request, "index.html", {'userProfile': loggedUserProfile, 'data': feed, 'sugProfileList': sugList})
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
        cnt = cnt+1
    # Get my follwing's posts

    for followingContactI in followingContactList:

        followingProfile = followingContactI.following

        postListI = followingProfile.posts.all()
        avatar_url = followingProfile.profileimage.url
        postUserName = followingProfile.userName
        if (postListI):
            for item in postListI:
                if cnt == 5:
                    return render(request, "index.html", {'userProfile': loggedUserProfile, 'data': feed, 'sugProfileList': sugList})
                dto = None
                # Bad
                # likedPostUserIds = {
                #     li.profile.userId for li in item.likes.all()}

                # Good : use join with select_related instead to reduce number of query
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
                cnt = cnt+1

    return render(request, "index.html", {'userProfile': loggedUserProfile, 'data': feed, 'sugProfileList': sugList})


@login_required
def settings(request):

    # Use get() for get exactly single one
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
                # use Signal for creating new profile after creating user
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
    try:
        if request.method == 'POST':
            userName = request.user.username
            image = request.FILES.get('image_upload')
            caption = request.POST['caption']

            newPost = Post.objects.create(
                image=image, caption=caption, profile=request.user.profile)
            return redirect('/')
        else:
            return redirect('/')
    except Exception as e:
        return redirect("/p500")


def like_post(request):
    loggedUserProfile = request.user.profile
    postId = request.POST['postId']
    # Use get() for get single one
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

    try:
        loggedUserProfile = request.user.profile
        # Good : use join with prefetch_related instead to reduce number of query after that
        userProfile = Profile.objects.prefetch_related(
            "posts").get(userName=pk)
        userPosts = userProfile.posts.all()
        userPostsLen = len(userPosts)

        if Contact.objects.filter(follower=loggedUserProfile, following=userProfile).first():
            buttonText = 'Unfollow'
        else:
            buttonText = 'Follow'

        followerCount = len(Contact.objects.filter(following=userProfile))
        followingCount = len(Contact.objects.filter(follower=userProfile))
        context = {

            'userProfile': userProfile,
            'userPosts': userPosts,
            'userPostsLen': userPostsLen,
            'buttonText': buttonText,
            'followerCount': followerCount,
            'followingCount': followingCount,

        }
        return render(request, "profile.html", context)
    except Exception as e:
        return redirect("/p404")


@login_required(login_url='signin')
def follow(request):
    try:
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
    except Exception as e:
        return redirect("/p500")


def search(request):
    # Use get() for get single one
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
    # get body payload
    content = request.POST["content"]
    postId = request.POST["postId"]

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

    # also can filter pk with parent instace in model
    commentsWithProfile = Comment.objects.filter(
        post=pk).select_related("profile")
    data = []
    loggedUserProfile = request.user.profile
    for item in commentsWithProfile:
        if item.profile == loggedUserProfile:
            # returning HTML help client dont need to use if statement
            data.append({"item": model_to_dict(item), "authUserName": item.profile.userName,
                         "authImg": item.profile.profileimage.url, "optionHTML": "<div class='dropdown'> <i role='button' class ='fa fa-ellipsis-h' type='button' data-toggle='dropdown' aria-expanded='false'> </i> <div class ='dropdown-menu'><span class='dropdown-item editCommentBtn'> Edit comment </span> <span class='dropdown-item deleteCommentBtn'> Delete comment <span></div> </div>"})
        else:
            data.append({"item": model_to_dict(item), "authUserName": item.profile.userName,
                         "authImg": item.profile.profileimage.url, "optionHTML": ""})
    # return JsonResponse(status=200, data={'comments': list(comments.values())}, safe=False)

    return JsonResponse(data, safe=False)


def ajaxFollow(request, userNameToFollow):

    loggedUserProfile = request.user.profile
    # must exist should use get()
    otherProfile = Profile.objects.get(userName=userNameToFollow)

    # no matter exist or not exist, can use filter(because fitler dont throw exception)
    oldFollow = Contact.objects.filter(follower=loggedUserProfile,
                                       following=otherProfile).first()

    if oldFollow:
        return JsonResponse(status=400, data={'message': 'Follow existed'})

    newFollow = Contact.objects.create(
        follower=loggedUserProfile, following=otherProfile)
    return JsonResponse(status=200, data={'message': 'follow success'})

    # error page:


def p500(request):
    # bad request
    return render(request, 'p500.html')


def p404(request):
    # page not found
    return render(request, 'p404.html')
