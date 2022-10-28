from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.models import User, auth
from django.contrib import messages


def index(request):
    return render(request, "index.html")


def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        print(username)
        password = request.POST["password"]
        confirmPassword = request.POST["confirmPassword"]
        if password == confirmPassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                return redirect("/")
        else:
            messages.info(request, "Password not matching")
            return redirect('signup')

        print(password)
    else:
        return render(request, 'signup.html')
