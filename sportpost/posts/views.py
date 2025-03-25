from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponseForbidden,HttpResponse
from .forms import PostForm
from .models import Post
from django.contrib.auth.models import User
from matches.models import Match
from django.utils import timezone
import datetime



# Create your views here.
def home_view(request:HttpRequest):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    matches = Match.objects.filter(date__in=[today, yesterday]).order_by("-time")
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
def delete_post(request:HttpRequest,id:int):
    if request.method=="POST":
        post=Post.objects.get(pk=id)
        if request.user==post.user:
            post.delete()
            if request.headers.get("HX-Request"):
                return HttpResponse("")
            return HttpResponse("Deleted")
    else:
        return HttpResponse("Method not allowed", status=405)
def detail_post_view(request,id):
    post=Post.objects.get(pk=id)
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    matches = Match.objects.filter(date__in=[today, yesterday]).order_by("-time") 
    return render(request,"posts/detail_post.html",{"post":post,"matches":matches,"detail_view": True})



        

    