from django.shortcuts import render,redirect
from .models import Match
from django.utils import timezone
import datetime


# Create your views here.
def live_score_view(request):
    today = datetime.datetime.now().strftime ("%Y-%m-%d")

    
    matches=Match.objects.all().filter(date=today).order_by("-time")
    return render(request,"matches/live_score.html",{"matches":matches})

