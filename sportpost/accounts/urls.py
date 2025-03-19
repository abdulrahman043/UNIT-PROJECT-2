from django.urls import path
from . import views
app_name="accounts"
urlpatterns = [
    path("register/",views.create_account_view,name="create_account_view"),
        path("login/",views.login_account_view,name="login_account_view"),
                path("logout/",views.logout_account,name="logout_account"),



  
       

]
