from django.urls import path
from .views import user_list, register, login, profile, delete_profile_photo

urlpatterns = [
    path("", user_list, name="user_list"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("profile/", profile, name="profile"),
    path("profile/photo/", delete_profile_photo, name="delete-profile-photo"),
]