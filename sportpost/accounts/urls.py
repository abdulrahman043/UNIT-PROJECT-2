from django.urls import path
from . import views
app_name="accounts"
urlpatterns = [
    path("register/",views.create_account_view,name="create_account_view"),
        path("login/",views.login_account_view,name="login_account_view"),
        path("logout/",views.logout_account,name="logout_account"),
        path("profile/<username>/post",views.profile_posts_view,name="profile_view"),
                path("profile/<username>/replys",views.profile_replys_view,name="profile_replys_view"),
                                path("profile/<username>/likes",views.profile_likes_view,name="profile_likes_view"),


        path("edit_profile/",views.edit_profile_view,name="edit_profile_view"),
        path("edit_profile/update",views.update_profile,name="update_profile"),
        path("bookmark",views.bookmark_view,name="bookmark_view"),
        path('bookmark/<post_id>',views.add_bookmark,name="add_bookmark"),
           path("like",views.like_view,name="like_view"),
        path('like/<post_id>',views.add_like,name="add_like"),
        path('repost/<post_id>',views.add_repost,name="add_repost"),
        path('search/',views.search_user_view,name="search_user_view"),
        path("notification/",views.notification_view,name="notification_view"),
        path("add_follow/<username>",views.add_delate_follow,name="add_delate_follow"),
        path("<username>/follwing/",views.user_following_view,name="user_following_view"),
                path("<username>/followers/",views.user_followers_view,name="user_followers_view"),






  
       

]
