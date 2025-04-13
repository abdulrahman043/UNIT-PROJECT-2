from django.shortcuts import render,redirect,get_object_or_404
from .models import Match
from django.utils import timezone
import datetime
from django.http import HttpRequest,HttpResponse,HttpResponseNotFound
from accounts.models import Notification
from django.contrib.auth.models import User
# Create your views here.
def live_score_view(request:HttpRequest):
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().astimezone().date()
    else:
        selected_date = timezone.now().astimezone().date()
    if not selected_date:
        selected_date = timezone.now().astimezone().date()
    matches = Match.objects.filter(date=selected_date).order_by("time")
    
    return render(request, "matches/live_score.html", {"matches": matches,"selected_date":selected_date ,'with_score':True})
def live_score_basketball_view(request:HttpRequest):
    
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().astimezone().date()
    else:
        selected_date = timezone.now().astimezone().date()
    if not selected_date:
        selected_date = timezone.now().astimezone().date()
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
    users=User.objects.order_by("?")[0:3]

    return render(request, "matches/live_score_basketball.html", {"users":users,"matches": matches,"unread_count":unread_count,"selected_date":selected_date,'with_score':True,"days_list":days_list,"live_score":True})
def score(request:HttpRequest):
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().astimezone().date()
    else:
        selected_date = timezone.now().astimezone().date()
    if not selected_date:
        selected_date = timezone.now().astimezone().date()
    matches = Match.objects.filter(date=selected_date).order_by("time")
    
    return render(request, "matches/score.html", {"matches": matches,"selected_date":selected_date,'with_score':True})
def box_score_view(request:HttpRequest,game_id):
    try:
        match = Match.objects.get(game_id=game_id)
    except Match.DoesNotExist:
        return HttpResponseNotFound("Match not found.")
   
    users=User.objects.order_by("?")[0:3]
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().astimezone().date()
    else:
        selected_date = timezone.now().astimezone().date()

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
    return render(request,"matches/box_score_home_team.html",{"match":match,"unread_count":unread_count,"users":users,"matches":matches,"days_list":days_list,"selected_date":selected_date,'with_score':True})
def box_score_awayteam_view(request:HttpRequest,game_id):
    try:
        match = Match.objects.get(game_id=game_id)
    except Match.DoesNotExist:
        return HttpResponseNotFound("Match not found.")
   
    users=User.objects.order_by("?")[0:3]
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date =timezone.now().astimezone().date()
    else:
        selected_date =timezone.now().astimezone().date()

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
    return render(request,"matches/box_score_away_team.html",{"match":match,"unread_count":unread_count,"users":users,"matches":matches,"days_list":days_list,"selected_date":selected_date,'with_score':True})
