from django.urls import path
from . import views
app_name="accounts"
urlpatterns = [
    path("register/",views.create_account_view,name="create_account_view"),
        path("login/",views.login_account_view,name="login_account_view"),
        path("logout/",views.logout_account,name="logout_account"),
        path("profile/<username>",views.profile_view,name="profile_view"),
        path("edit_profile/",views.edit_profile_view,name="edit_profile_view"),
        path("edit_profile/update",views.update_profile,name="update_profile"),
        path("bookmark",views.bookmark_view,name="bookmark_view"),
        path('bookmark/<post_id>',views.add_bookmark,name="add_bookmark"),
           path("like",views.like_view,name="like_view"),
        path('like/<post_id>',views.add_like,name="add_like"),
        path('repost/<post_id>',views.add_repost,name="add_repost"),





  
       

]
