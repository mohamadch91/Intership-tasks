from django.urls import path
from .views import user_list, register, login, profile

urlpatterns = [
    path("", user_list, name="user_list"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("profile/", profile, name="profile"),
]