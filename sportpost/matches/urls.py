from django.urls import path
from . import views
app_name="matches"
urlpatterns = [
    path("score/",views.live_score_view,name="live_score_view"),
        path("score-only/",views.update_score_only,name="update_score_only"),

    

   
       
       

]
