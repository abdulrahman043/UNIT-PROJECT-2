from django.urls import path
from . import views
app_name="matches"
urlpatterns = [
    path("score/",views.live_score_view,name="live_score_view"),
        path("livescore/",views.live_score_basketball_view,name="live_score_basketball_view"),
            path("live_score/",views.score,name="score"),
                        path("<game_id>/box_score/",views.box_score_view,name="box_score_view"),
                                                path("<game_id>/box_score/awayTeam",views.box_score_awayteam_view,name="box_score_awayteam_view"),






    

   
       
       

]
