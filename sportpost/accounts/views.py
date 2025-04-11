from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import Profile,Bookmark,Like,Notification,Follow
from matches.models import Match
from django.http import HttpRequest,HttpResponse
from django.utils import timezone
import datetime
from posts.models import Post
from posts.views import is_liked,is_bookmarked
from django.db import transaction, IntegrityError
from posts.models import Post
from django.contrib import messages
from django.template.loader import render_to_string

# Create your views here.
def create_account_view(request:HttpRequest):
    if request.method=="POST":
        try:
            if len(request.POST["username"])<3 or len(request.POST["password"])<6:
                messages.error(request, "Username must be at least 3 characters long and password must be at least 6 characters long.")
                return render(request, "accounts/signup.html")

            user = User.objects.create_user(username=request.POST["username"], email=request.POST["email"], password=request.POST["password"])
            user.save()
            Profile.objects.create(user=user,name=request.POST["name"])
            messages.success(request, "Your account has been created successfully! Please log in.")
            return redirect("accounts:login_account_view")

        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
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
        else:
            messages.error(request, "Invalid username or password.") 


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
        follow=Follow.objects.filter(follower=request.user,following__username=username).exists()
    else:
        follow=None
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
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
    return render(request,"accounts/profile_reply.html",{"profile_bold":True,"posts":posts,"unread_count":unread_count,"is_following":follow,"matches":matches,"profile_replys_view":True,"profile":profile,"days_list":days_list,"selected_date":selected_date,"users":users})
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
        follow=Follow.objects.filter(follower=request.user,following__username=username).exists()
    else:
        follow=None

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
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
    return render(request,"accounts/profile_post.html",{"profile_bold":True,"posts":posts,"unread_count":unread_count,"matches":matches,"profile_post_view":True,"profile":profile,"days_list":days_list,"selected_date":selected_date,"users":users,"is_following":follow})
def profile_likes_view(request:HttpRequest,username):
    now = datetime.datetime.now()
    
    user=User.objects.get(username=username)
    profile=user.profile

    posts = Post.objects.filter(like__user=user).order_by("-created_at")
    if request.user.is_authenticated:
        posts=is_bookmarked(posts,request.user)
        posts=is_liked(posts,request.user)
        follow=Follow.objects.filter(follower=request.user,following__username=username).exists()
    else:
        follow=None
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
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
    return render(request,"accounts/profile_like.html",{"profile_bold":True,"posts":posts,"unread_count":unread_count,"is_following":follow,"matches":matches,"profile_likes_view":True,"profile":profile,"days_list":days_list,"selected_date":selected_date,"users":users})
def edit_profile_view(request:HttpRequest):
    return render(request,"accounts/edit_profile.html")
def add_delate_follow(request:HttpRequest,username):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    try:
        follow=Follow.objects.get(follower=request.user,following__username=username)
        follow.delete()
    except Follow.DoesNotExist:
        try:
            following=User.objects.get(username=username)
            follow=Follow.objects.get_or_create(follower=request.user,following=following)
        except:
            pass
    
    return redirect("accounts:profile_view", username)
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
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
    return render(request,"accounts/bookmark.html",{"matches":matches,"unread_count":unread_count,"is_bookmarked":True,"days_list":days_list,"selected_date":selected_date,"users":users})
def notification_view(request:HttpRequest):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    matches = Match.objects.filter(date__in=[today, yesterday]).order_by("-time") 
    notifications = Notification.objects.filter(receiver=request.user).order_by("-created_at")
    notifications.filter(is_read=False).update(is_read=True)
    
      
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
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
    return render(request,"accounts/notification.html",{"matches":matches,"unread_count":unread_count,"is_noti":True,"notifications":notifications,"days_list":days_list,"selected_date":selected_date,"users":users})



def add_bookmark(request: HttpRequest, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        bookmark = Bookmark.objects.filter(user=request.user, post=post).first()
        if bookmark:
            bookmark.delete()
        else:
            Bookmark.objects.create(user=request.user, post=post)
        
        is_bookmarked = Bookmark.objects.filter(user=request.user, post=post).exists()

        if request.headers.get("HX-Request"):
            context = {"post": post, "is_bookmarked": is_bookmarked}
            html = render_to_string("posts/_bookmark_button.html", context)
            return HttpResponse(html)
        
        return redirect("posts:home_view")
    
    return redirect("posts:home_view")

def like_view(request:HttpRequest):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    matches = Match.objects.filter(date__in=[today, yesterday]).order_by("-time") 
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
    return render(request,"accounts/like.html",{"matches":matches,"is_liked":True,'unread_count':unread_count})

def add_like(request:HttpRequest,post_id):
    if request.method=="POST":
        post=get_object_or_404(Post,pk=post_id)
        like=Like.objects.filter(user=request.user,post=post).first()
        if like:
            like.delete()
              
        else:
            print(1)
            Like.objects.create(user=request.user,post=post)
        is_liked=Like.objects.filter(user=request.user,post=post).exists()
        if request.headers.get("HX-Request"):
            context={"post":post,"is_liked":is_liked}
            html=render_to_string("posts/_like_button.html",context)
            return HttpResponse(html)



        return redirect('posts:home_view')
    return redirect('posts:home_view')



def add_repost(request: HttpRequest, post_id):
    
    if request.method == "POST":
        target_post = get_object_or_404(Post, pk=post_id)
        if target_post.repost_of:
            target_post = target_post.repost_of

        with transaction.atomic():
            existing_reposts = Post.objects.filter(
                user=request.user, repost_of=target_post
            )
            if existing_reposts.exists():
                existing_reposts.delete()
            else:
                try:
                    if target_post.game:
                        Post.objects.create(user=request.user, repost_of=target_post, content="",game=target_post.game)
                    else:
                        Post.objects.create(user=request.user, repost_of=target_post, content="")
                except IntegrityError:
                    pass
                  
        
        if request.headers.get("HX-Request"):
            is_reposted=Post.objects.filter(user=request.user,repost_of=target_post).exists()
            context={"post":target_post,"is_reposted":is_reposted}
            html = render_to_string("posts/_repost_button.html", context)
            return HttpResponse(html)
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
        
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
    return render(request,"accounts/search_user.html",{"users":users,"unread_count":unread_count,"matches":matches,"days_list":days_list,"selected_date":selected_date,"query":query,"in_search":True})
def user_following_view(request:HttpRequest,username):
    user=User.objects.get(username=username)
    profile=user.profile

    following = Follow.objects.filter(follower=user).values_list('following', flat=True)
    users=User.objects.filter(id__in=following)
    

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
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
    return render(request,"accounts/user_following.html",{"users":users,"unread_count":unread_count,"profile":profile,"matches":matches,"days_list":days_list,"selected_date":selected_date,"in_follow":True})
def user_followers_view(request:HttpRequest,username):
    user=User.objects.get(username=username)
    profile=user.profile

    following = Follow.objects.filter(following=user).values_list('follower', flat=True)
    users=User.objects.filter(id__in=following)
    

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
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
    return render(request,"accounts/user_following.html",{"users":users,"unread_count":unread_count,"profile":profile,"matches":matches,"days_list":days_list,"selected_date":selected_date,"in_follow":True})

        
        