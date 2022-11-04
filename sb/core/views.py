from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain


@login_required(login_url='signin')
def index(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    userName_following_list = []
    feed = []

    userName_following_list = FollowersCount.objects.filter(
        follower=request.user.username)
    for userNamei in userName_following_list:
        post_listi = Post.objects.filter(userName=userNamei)
        if(post_listi):
            avatar_url = post_listi[0].auth.profile.profileimage.url
            for item in post_listi:
                dto = {'postContent': item, 'postAuthAvatar': avatar_url}
                feed.append(dto)
    # each item in array to a parameter in chain method
    # feed_list = list(chain(*feed))

    allUser = User.objects.all()
    userFollowing = []
    userFollowing.append(request.user)
    for usernamei in userName_following_list:
        if User.objects.filter(username=usernamei).exists():
            followingUserI = User.objects.get(username=usernamei)
            userFollowing.append(followingUserI)
    sugList = [x for x in list(allUser) if (x not in list(userFollowing))]

    sugProfileList = []
    for sugUser in sugList:
        sugProfileList.append(sugUser.profile)

    # posts = Post.objects.all()

    print(sugProfileList)
    return render(request, "index.html", {'user_profile': user_profile, 'data': feed, 'sugProfieList': sugProfileList})


@login_required
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if(request.method == "POST"):
        image = None
        if request.FILES.get('image') == None:
            image = user_profile.profileimage
        else:
            image = request.FILES.get('image')
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimage = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})


def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        print(username)
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
                new_profile = Profile.objects.create(
                    user=user, userId=user.id)
                new_profile.save()
                return redirect("/signin")
        else:
            messages.info(request, "Password not matching")
            return redirect('signup')

        print(password)
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

        newPost = Post.objects.create(userName=userName,
                                      image=image, caption=caption, auth=request.user)
        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')
def like_post(request):
    userName = request.user.username
    # use get() for param
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(
        post_id=post_id, userName=userName).first()
    if like_filter == None:
        newLike = LikePost.objects.create(post_id=post_id, userName=userName)
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')


@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(userName=pk)
    user_posts_length = len(user_posts)

    follower = request.user.username
    if FollowersCount.objects.filter(follower=follower, userName=pk):
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    followerCount = len(FollowersCount.objects.filter(userName=pk))
    followingCount = len(FollowersCount.objects.filter(follower=pk))
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_posts_length': user_posts_length,
        'button_text': button_text,
        'followerCount': followerCount,
        'followingCount': followingCount,

    }
    return render(request, "profile.html", context)


@login_required(login_url='signin')
def follow(request):
    if request.method == "POST":
        follower = request.POST["follower"]
        userName = request.POST["userName"]

        oldFollower = FollowersCount.objects.filter(
            follower=follower, userName=userName).first()

        if(oldFollower):

            delete_follower = oldFollower.delete()
            return redirect("/profile/"+userName)
        else:

            new_follower = FollowersCount.objects.create(
                follower=follower, userName=userName)
            return redirect("/profile/"+userName)

    else:
        return redirect("/")


def search(request):
    user_object = User.objects.get(username=request.user.username)

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

def profile_demo(request,pk):
    user_obj = User.objects.filter(username=pk)
    return render(request,'profile_demo.html',{
        "user_obj":user_obj
    })