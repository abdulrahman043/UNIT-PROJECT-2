from django.shortcuts import render,redirect,get_object_or_404
from .models import Match
from django.utils import timezone
import datetime
from django.http import HttpRequest,HttpResponse

# Create your views here.
def live_score_view(request:HttpRequest):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    selected_date=request.GET.get("match_date")
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    order_matches=Match.objects.order_by('date').values_list('date',flat=True).distinct()
    if not selected_date:
        selected_date = timezone.now().date()
    print(selected_date)
    matches = Match.objects.filter(date=selected_date).order_by("time")
    print(matches)
    
    return render(request, "matches/live_score.html", {"matches": matches,"selected_date":selected_date})
def update_score_only(request):
    match_id = request.GET.get("match_id")
    side = request.GET.get("side")
    
    if not match_id or not side:
        return HttpResponse("Missing parameters.", status=400)
    
    match = get_object_or_404(Match, pk=match_id)
    
    # Determine which score to return
    if side == "home":
        return HttpResponse(match.home_score)
    elif side == "away":
        return HttpResponse(match.away_score)
    else:
        return HttpResponse("Invalid 'side'.", status=400)