from django.shortcuts import render,redirect
from django.http import HttpRequest
from .forms import PostForm
from .models import Post
from django.contrib.auth.models import User
from matches.models import Match


# Create your views here.
def home_view(request:HttpRequest):
    matches=Match.objects.all().order_by("-time")
    posts=Post.objects.all().order_by('-created_at')
    return render(request,"posts/home.html",{"posts":posts,"matches":matches})
def add_post(request:HttpRequest):
    if not request.user.is_authenticated:
        return redirect("accounts:create_account_view")
    if request.method=="POST":
        post_form=PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()


            return redirect("posts:home_view")
        

    