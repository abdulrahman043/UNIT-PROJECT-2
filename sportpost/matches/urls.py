from django.urls import path
from . import views
app_name="matches"
urlpatterns = [
    path("score/",views.live_score_view,name="live_score_view"),
        path("livescore/",views.live_score_basketball_view,name="live_score_basketball_view"),


    

   
       
       

]
