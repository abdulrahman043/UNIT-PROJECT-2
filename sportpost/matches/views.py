from django.shortcuts import render,redirect,get_object_or_404
from .models import Match
from django.utils import timezone
import datetime
from django.http import HttpRequest,HttpResponse
from accounts.models import Notification
# Create your views here.
def live_score_view(request:HttpRequest):
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    if not selected_date:
        selected_date = timezone.now().date()
    matches = Match.objects.filter(date=selected_date).order_by("time")
    
    return render(request, "matches/live_score.html", {"matches": matches,"selected_date":selected_date ,'with_score':True})
def live_score_basketball_view(request:HttpRequest):
    
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    if not selected_date:
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
    
    return render(request, "matches/live_score_basketball.html", {"matches": matches,"unread_count":unread_count,"selected_date":selected_date,'with_score':True,"days_list":days_list,"live_score":True})
def score(request:HttpRequest):
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    if not selected_date:
        selected_date = timezone.now().date()
    matches = Match.objects.filter(date=selected_date).order_by("time")
    
    return render(request, "matches/score.html", {"matches": matches,"selected_date":selected_date,'with_score':True})