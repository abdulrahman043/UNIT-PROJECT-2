from django.shortcuts import render
from .models import Match

# Create your views here.
def live_score_view(request):
    matches=Match.objects.all().order_by("-time")
    print(matches)
    return render(request,"matches/live_score.html",{"matches":matches})
