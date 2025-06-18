from django.urls import path, re_path
from userapp import views as vw 

urlpatterns = [
    re_path(r'^profile/(?P<userId>\d+)/', vw.user_profile, name="profile"),
    re_path(r'^edit_profile/(?P<userId>\d+)/', vw.edit_profile, name= "edit_profile"),
    re_path(r'^deactivate_profile/(?P<userId>\d+)/', vw.deactivate_profile, name="deactivate_profile"),
    re_path(r'^all_user/(?P<status>\w+)/', vw.display_users, name="all_user"),
    re_path(r'^delete_profile/(?P<userId>\d+)/', vw.delete_profile, name="delete_profile"),
    
]