from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.http import HttpRequest

# Create your views here.
def create_account_view(request:HttpRequest):
    if request.method=="POST":
        try:
            user = User.objects.create_user(username=request.POST["username"], email=request.POST["email"], password=request.POST["password"])
            user.save()
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
    
    