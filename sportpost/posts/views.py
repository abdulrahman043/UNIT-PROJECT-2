from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponseForbidden,HttpResponse
from .forms import PostForm
from .models import Post
from django.contrib.auth.models import User
from matches.models import Match
from django.utils import timezone
import datetime
from accounts.models import Bookmark,Like

from django.db.models import Exists, OuterRef


# Create your views here.
def home_view(request:HttpRequest):
   
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()

    order_matches=Match.objects.order_by('date').values_list('date',flat=True).distinct()
    
    days_list=[]
    for day in order_matches:
        day_dict = {
        "date": day,
        "is_selected": (day == selected_date),  
        "day_name": day.strftime("%a")           
    }
        days_list.append(day_dict)
    matches = Match.objects.filter(date=selected_date).order_by("time")

    posts=Post.objects.all().order_by('-created_at')
    if request.user.is_authenticated:
        posts=is_bookmarked(posts,request.user)
        posts=is_liked(posts,request.user)
        posts=is_reposted(posts,request.user)
    return render(request,"posts/home.html",{"posts":posts,"matches":matches,"days_list":days_list,"selected_date":selected_date})
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
def add_replay(request:HttpRequest,id:int):
    if not request.user.is_authenticated:
        return redirect("accounts:create_account_view")
    if request.method=="POST":
        post=Post.objects.get(pk=id)
        replay_post=Post.objects.create(user=request.user,content=request.POST["content"],parent_post=post)
        return redirect("posts:detail_post_view", id=post.id)


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
    replies = post.replies.all()

    return render(request,"posts/detail_post.html",{"post":post,"matches":matches,"detail_view": True,"replies":replies})



def search_view(request:HttpRequest):
    query=request.GET.get("q")
    if query:
        users=User.objects.filter(username__contains=query)[0:3]
        posts=Post.objects.filter(content__contains=query).order_by('-created_at')
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()

    order_matches=Match.objects.order_by('date').values_list('date',flat=True).distinct()
    
    days_list=[]
    for day in order_matches:
        day_dict = {
        "date": day,
        "is_selected": (day == selected_date),  
        "day_name": day.strftime("%a")           
    }
        days_list.append(day_dict)
    matches = Match.objects.filter(date=selected_date).order_by("time")
        
    
    return render(request,"posts/search.html",{"users":users,"posts":posts,"matches":matches,"days_list":days_list,"selected_date":selected_date,"query":query,"in_search":True})

def is_bookmarked(posts, user):
    try:
        if user.is_authenticated:
            bookmark_subquery = Bookmark.objects.filter(
                user=user,        # Filter bookmarks for the current user
                post=OuterRef('pk')  # Compare each post's primary key with the bookmark's post
            )
            return posts.annotate(is_bookmarked=Exists(bookmark_subquery))
        else:
            return posts.annotate(is_bookmarked=False)
    except Exception as e:
        print(e)
def is_liked(posts, user):
    try:
        if user.is_authenticated:
            like_subquery = Like.objects.filter(
                user=user,       
                post=OuterRef('pk')  
            )
            return posts.annotate(is_liked=Exists(like_subquery))
        else:
            return posts.annotate(is_liked=False)
    except Exception as e:
        print(e)
def is_reposted(posts, user):
    try:
        if user.is_authenticated:
            repost_subquery = Post.objects.filter(
                user=user,              # Check reposts by the current user
                repost_of=OuterRef('pk')  # Compare against the original post's primary key
            )
            return posts.annotate(is_reposted=Exists(repost_subquery))
        else:
            return posts.annotate(is_reposted=False)
    except Exception as e:
        print(e)

def game_post_view(request:HttpRequest,game_id):
    return render(request,"posts/game_post.html")