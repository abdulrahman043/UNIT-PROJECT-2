from django.shortcuts import render,redirect,get_object_or_404
from .models import Match
from django.utils import timezone
import datetime
from django.http import HttpRequest,HttpResponse

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
    
    return render(request, "matches/live_score.html", {"matches": matches,"selected_date":selected_date})
