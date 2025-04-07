from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import Profile,Bookmark,Like,Notification
from matches.models import Match
from django.http import HttpRequest,HttpResponse
from django.utils import timezone
import datetime
from posts.models import Post
from posts.views import is_liked,is_bookmarked
from django.db import transaction, IntegrityError
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
def profile_replys_view(request:HttpRequest,username):
    
    user=User.objects.get(username=username)
    profile=user.profile
    
    posts = Post.objects.filter(user=user, parent_post__isnull=False).order_by("-created_at")
    if request.user.is_authenticated:
        posts=is_bookmarked(posts,request.user)
        posts=is_liked(posts,request.user)
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
    users=User.objects.order_by("?")[0:3]
    return render(request,"accounts/profile_reply.html",{"posts":posts,"matches":matches,"profile_replys_view":True,"profile":profile,"days_list":days_list,"selected_date":selected_date,"users":users})
def profile_posts_view(request:HttpRequest,username):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    user=User.objects.get(username=username)
    profile=user.profile
    
    posts = Post.objects.filter(user=user, parent_post__isnull=True).order_by("-created_at")
    if request.user.is_authenticated:
        posts=is_bookmarked(posts,request.user)
        posts=is_liked(posts,request.user)
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
    users=User.objects.order_by("?")[0:3]
    return render(request,"accounts/profile_post.html",{"posts":posts,"matches":matches,"profile_post_view":True,"profile":profile,"days_list":days_list,"selected_date":selected_date,"users":users})
def profile_likes_view(request:HttpRequest,username):
    now = datetime.datetime.now()
    
    user=User.objects.get(username=username)
    profile=user.profile
    posts = Post.objects.filter(like__user=user).order_by("-created_at")
    if request.user.is_authenticated:
        posts=is_bookmarked(posts,request.user)
        posts=is_liked(posts,request.user)
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
    users=User.objects.order_by("?")[0:3]
    return render(request,"accounts/profile_like.html",{"posts":posts,"matches":matches,"profile_likes_view":True,"profile":profile,"days_list":days_list,"selected_date":selected_date,"users":users})
def edit_profile_view(request:HttpRequest):
    return render(request,"accounts/edit_profile.html")
def update_profile(request:HttpRequest):
    if request.method=="POST":
        profile = request.user.profile
        profile.name=request.POST["name"]
        profile.bio=request.POST["bio"]
        if "profile_image" in request.FILES:
            profile.profile_image = request.FILES["profile_image"]
        profile.save()

        return redirect("accounts:profile_view", username=request.user.username)



def bookmark_view(request:HttpRequest):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    matches = Match.objects.filter(date__in=[today, yesterday]).order_by("-time") 
      
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
    users=User.objects.order_by("?")[0:3]
    return render(request,"accounts/bookmark.html",{"matches":matches,"is_bookmarked":True,"days_list":days_list,"selected_date":selected_date,"users":users})
def notification_view(request:HttpRequest):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    matches = Match.objects.filter(date__in=[today, yesterday]).order_by("-time") 
    notifications = request.user.receiver.all()
      
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
    users=User.objects.order_by("?")[0:3]
    return render(request,"accounts/notification.html",{"matches":matches,"is_noti":True,"notifications":notifications,"days_list":days_list,"selected_date":selected_date,"users":users})

def add_bookmark(request:HttpRequest,post_id):
    if request.method=="POST":
        post=Post.objects.get(pk=post_id)
        bookmark=Bookmark.objects.filter(user=request.user,post=post).first()
        if bookmark:
            bookmark.delete()
            if request.headers.get("HX-Request"):
                return HttpResponse('''<svg  id="bookmark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0 1 11.186 0Z" />
        </svg>''')
            
        else:
            Bookmark.objects.create(user=request.user,post=post)
            if request.headers.get("HX-Request"):
                return HttpResponse('''<svg  id="bookmark" xmlns="http://www.w3.org/2000/svg" fill="blue" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0 1 11.186 0Z" />
        </svg>''')
          

        return redirect('posts:home_view')
    
    return redirect('posts:home_view')

def like_view(request:HttpRequest):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    matches = Match.objects.filter(date__in=[today, yesterday]).order_by("-time") 
    
    return render(request,"accounts/like.html",{"matches":matches,"is_liked":True})

def add_like(request:HttpRequest,post_id):
    if request.method=="POST":
        post=Post.objects.get(pk=post_id)
        like=Like.objects.filter(user=request.user,post=post).first()
        if like:
            like.delete()
            if request.headers.get("HX-Request"):
                return HttpResponse('''   <svg  id="like-{{post.id}}"  xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
        </svg>''')    
        else:
            Like.objects.create(user=request.user,post=post)
            if request.headers.get("HX-Request"):
                return HttpResponse('''   <svg  id="like-{{post.id}}"  xmlns="http://www.w3.org/2000/svg" fill="red" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
        </svg>''')
        return redirect('posts:home_view')
    return redirect('posts:home_view')



def add_repost(request: HttpRequest, post_id):
    if request.method == "POST":
        target_post = get_object_or_404(Post, pk=post_id)
        if target_post.repost_of:
            target_post = target_post.repost_of

        with transaction.atomic():
            existing_reposts = Post.objects.select_for_update().filter(
                user=request.user, repost_of=target_post
            )
            if existing_reposts.exists():
                existing_reposts.delete()
                action = "removed"
            else:
                try:
                    Post.objects.create(user=request.user, repost_of=target_post, content="")
                    action = "added"
                except IntegrityError:
                    return HttpResponse("Repost failed due to duplicate.", status=400)
        
        if request.headers.get("HX-Request"):
            if action == "removed":
                return HttpResponse('''
                    <svg id="repost-{{ post_id }}" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" 
                              d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 0 0-3.7-3.7 48.678 48.678 0 0 0-7.324 0 4.006 4.006 0 0 0-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 0 0 3.7 3.7 48.656 48.656 0 0 0 7.324 0 4.006 4.006 0 0 0 3.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3-3 3" />
                    </svg>
                ''')
            else:
                return HttpResponse('''
                    <svg id="repost-{{ post_id }}" xmlns="http://www.w3.org/2000/svg" fill="green" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" 
                              d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 0 0-3.7-3.7 48.678 48.678 0 0 0-7.324 0 4.006 4.006 0 0 0-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 0 0 3.7 3.7 48.656 48.656 0 0 0 7.324 0 4.006 4.006 0 0 0 3.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3-3 3" />
                    </svg>
                ''')
        return redirect('posts:home_view')
    return redirect('posts:home_view')
def search_user_view(request:HttpRequest):
    query=request.GET.get("q")
    if query:
        users=User.objects.filter(username__contains=query)
    else:
        users=User.objects.order_by("?")[0:100]
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
        
    
    return render(request,"accounts/search_user.html",{"users":users,"matches":matches,"days_list":days_list,"selected_date":selected_date,"query":query,"in_search":True})