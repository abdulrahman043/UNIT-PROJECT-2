from django.urls import path
from . import views
app_name="posts"
urlpatterns = [
   path("",views.home_view ,name="home_view", ),
    path("add/",views.add_post,name="add_post"),
        path("delete/<id>",views.delete_post,name="delete_post"),
         path("detail/<id>",views.detail_post_view,name="detail_post_view")


]
htmx_urlpatterns=[
    
]
urlpatterns+=htmx_urlpatterns