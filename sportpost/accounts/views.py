from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import Profile
from matches.models import Match
from django.http import HttpRequest
from django.utils import timezone
import datetime
from posts.models import Post
# Create your views here.
def create_account_view(request:HttpRequest):
    if request.method=="POST":
        try:
            print(request.POST)
            user = User.objects.create_user(username=request.POST["username"], email=request.POST["email"], password=request.POST["password"])
            user.save()
            Profile.objects.create(user=user,name=request.POST["name"])
            
            return redirect("accounts:login_account_view")

        except Exception as e:
            print(e)

    return render(request,"accounts/signup.html")
def login_account_view(request:HttpRequest):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("posts:home_view")


    return render(request,"accounts/login.html")
    
def logout_account(request:HttpRequest):
    logout(request)
    return redirect('posts:home_view')
def profile_view(request:HttpRequest,username):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    matches = Match.objects.filter(date__in=[today, yesterday]).order_by("-time") 
    user=User.objects.get(username=username)
    
    posts=Post.objects.filter(user=user)
    return render(request,"accounts/profile.html",{"posts":posts,"matches":matches,"profile_view":True})
def edit_profile_view(request:HttpRequest):
  
    return render(request,"accounts/edit_profile.html")