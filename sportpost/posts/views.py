from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponseForbidden,HttpResponse,HttpResponseNotFound
from .forms import PostForm
from .models import Post
from django.contrib.auth.models import User
from matches.models import Match
from django.utils import timezone
import datetime
from accounts.models import Bookmark,Like,Follow,Notification
from django.db.models import Q

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
    users=User.objects.order_by("?")[0:3]
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None

    posts=Post.objects.all().order_by('-created_at')
    if request.user.is_authenticated:
        posts=is_bookmarked(posts,request.user)
        posts=is_liked(posts,request.user)
        posts=is_reposted(posts,request.user)

    if request.user.is_authenticated:
        user=User.objects.get(username=request.user.username)
        following = Follow.objects.filter(follower=user).values_list('following', flat=True)
        following_user=User.objects.filter(id__in=following)
    else:
        following_user=None
    return render(request,"posts/home.html",{"home_bold":True,"posts":posts,'with_score':True,"unread_count":unread_count,"following_user":following_user,"matches":matches,"days_list":days_list,"selected_date":selected_date,"users":users})
def home_following_view(request:HttpRequest):
    if not request.user.is_authenticated:
        return redirect('accounts:login_account_view')
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()

    order_matches=Match.objects.order_by('date').values_list('date',flat=True).distinct()
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
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
    following_ids=Follow.objects.filter(follower=request.user).values_list('following__id',flat=True)
    posts=Post.objects.filter(Q(user__id__in=following_ids)|Q(user__id=request.user.id)).order_by('-created_at')
    
    if request.user.is_authenticated:
        posts=is_bookmarked(posts,request.user)
        posts=is_liked(posts,request.user)
        posts=is_reposted(posts,request.user)

    return render(request,"posts/home_following.html",{"home_bold":True,"posts":posts,"unread_count":unread_count,'with_score':True,"matches":matches,"days_list":days_list,"selected_date":selected_date,"users":users})
def add_post(request:HttpRequest):
    
    game_id=request.GET.get("id")
    if request.method=="POST":
        if "image" in request.FILES:
            post_form=PostForm(request.POST,request.FILES)
        else:
            post_form=PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            if game_id:
                match=Match.objects.get(game_id=game_id)
                post.game=match
                post.save()
                return redirect("posts:game_post_view",game_id)
            else:
                post.save()
            return redirect("posts:home_view")
def add_replay(request:HttpRequest,id:int):
    if not request.user.is_authenticated:
        return redirect("accounts:create_account_view")
    if request.method=="POST":
        post=Post.objects.get(pk=id)
        if post.game:
            if "image" in request.FILES:
                replay_post=Post.objects.create(user=request.user,content=request.POST["content"],parent_post=post,image=request.FILES["image"],game=post.game)
            else:
                replay_post=Post.objects.create(user=request.user,content=request.POST["content"],parent_post=post,game=post.game)
        else:
            if "image" in request.FILES:
                replay_post=Post.objects.create(user=request.user,content=request.POST["content"],parent_post=post,image=request.FILES["image"])
            else:
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
    post=Post.objects.filter(pk=id)
    if request.user.is_authenticated:
        post= is_bookmarked(post, request.user)
        post = is_liked(post, request.user)
        post = is_reposted(post, request.user)
        post = post.first()
    replies = post.replies.all()
    
    
    if request.user.is_authenticated:
        replies=is_bookmarked(replies,request.user)
        replies=is_liked(replies,request.user)
        replies=is_reposted(replies,request.user)
       
    
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
    
    return render(request,"posts/detail_post.html",{"post":post,"unread_count":unread_count,"matches":matches,"detail_view": True,"replies":replies,"days_list":days_list,"selected_date":selected_date,"users":users,"id":str(id)})



def search_view(request:HttpRequest):
    query=request.GET.get("q")
    if query:
        users=User.objects.filter(username__contains=query)[0:3]
        posts=Post.objects.filter(content__contains=query).order_by('-created_at')
    else:
        posts=None
        users=None
    
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None    

    return render(request,"posts/search.html",{"users":users,"unread_count":unread_count,"posts":posts,"query":query,"in_search":True,"users":users})

def is_bookmarked(posts, user):
    try:
        if user.is_authenticated:
            bookmark_subquery = Bookmark.objects.filter(
                user=user,        
                post=OuterRef('pk')  
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
    try:
        match = Match.objects.get(game_id=game_id)
    except Match.DoesNotExist:
        return HttpResponseNotFound("Match not found.")
    posts=Post.objects.filter(game_id=game_id).order_by('-created_at')
    users=User.objects.order_by("?")[0:3]
    if request.user.is_authenticated:
        posts=is_bookmarked(posts,request.user)
        posts=is_liked(posts,request.user)
        posts=is_reposted(posts,request.user)
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
    return render(request,"posts/game_post.html",{"home_bold":True,"match":match,"unread_count":unread_count,'with_score':True,"posts":posts,"game_post":True,"users":users,"matches":matches,"days_list":days_list,"selected_date":selected_date})
def game_post_following_view(request:HttpRequest,game_id):
    if not request.user.is_authenticated:
        return redirect("accounts:create_account_view") 
    try:
        match = Match.objects.get(game_id=game_id)
    except Match.DoesNotExist:
        return HttpResponseNotFound("Match not found.")
    following_ids=Follow.objects.filter(follower=request.user).values_list('following__id',flat=True)
    posts=Post.objects.filter((Q(game_id=game_id) & Q(user__id__in=following_ids ))| (Q(user__id=request.user.id)&Q(game_id=game_id))).order_by('-created_at')
    users=User.objects.order_by("?")[0:3]
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
    if request.user.is_authenticated:
        posts=is_bookmarked(posts,request.user)
        posts=is_liked(posts,request.user)
        posts=is_reposted(posts,request.user)
    try:
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    except:
        unread_count=None
    return render(request,"posts/game_post_following.html",{"home_bold":True,"match":match,"unread_count":unread_count,"posts":posts,"game_post":True,"users":users,"matches":matches,"days_list":days_list,"selected_date":selected_date,'with_score':True})
