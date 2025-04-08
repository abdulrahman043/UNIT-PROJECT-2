from django.urls import path
from . import views
app_name="posts"
urlpatterns = [
   path("",views.home_view ,name="home_view" ),
      path("following/",views.home_following_view ,name="home_following_view" ),

    path("add/post",views.add_post,name="add_post"),
        path("delete/<id>",views.delete_post,name="delete_post"),
         path("detail/<id>",views.detail_post_view,name="detail_post_view"),
             path("add/replay/<id>",views.add_replay,name="add_replay"),
    path("search",views.search_view,name="search_view"),
    path("<game_id>/",views.game_post_view,name="game_post_view"),
        path("<game_id>/following",views.game_post_following_view,name="game_post_following_view")




]