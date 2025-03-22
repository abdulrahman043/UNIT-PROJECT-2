from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import Profile

from django.http import HttpRequest

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
def profile_view(requset,username):
    return render(requset,"accounts/profile.html")