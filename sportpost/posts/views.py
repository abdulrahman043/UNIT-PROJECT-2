from django.shortcuts import render,redirect
from django.http import HttpRequest
from .forms import PostForm
from .models import Post

# Create your views here.
def home_view(request:HttpRequest):
    posts=Post.objects.all()
    return render(request,"posts/home.html",{"posts":posts})
def add_post(request:HttpRequest):
    
    if request.method=="POST":
        post_form=PostForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect("posts:home_view")
        

    