from django.urls import path
from .views import user_list, register

urlpatterns = [
    path("", user_list, name="user_list"),
    path("register/", register, name="register"),
]