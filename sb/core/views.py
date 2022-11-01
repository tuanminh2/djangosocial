from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post


def index(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        return render(request, "index.html", {'user_profile': user_profile})
    else:
        return redirect("/signin")


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
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                # savedUser = user.save()
                new_profile = Profile.objects.create(
                    user=user, userId=user.id)
                new_profile.save()
                return redirect("/")
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
                                      image=image, caption=caption)
        return redirect('/')
    else:
        return redirect('/')

    return HttpResponse('<h1>upload get route</h1>')
