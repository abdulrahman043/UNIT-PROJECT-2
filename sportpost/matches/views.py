from django.shortcuts import render,redirect
from .models import Match
from django.utils import timezone
import datetime


# Create your views here.
def live_score_view(request):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    matches = Match.objects.filter(date__in=[today, yesterday]).order_by("-time")
    
    return render(request, "matches/live_score.html", {"matches": matches})
