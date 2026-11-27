from django.urls import path
from . import views

urlpatterns = [
    path("", views.book, name="book"),
    path("<int:pk>/", views.book_detail, name="book-detail"),
]