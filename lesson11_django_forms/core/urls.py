from django.urls import path
from . import views

urlpatterns = [
    path("", views.movie_list, name="movieList"),
    path("add/", views.movie_add, name="movieAdd"),
    path("<int:pk>/", views.movie_detail, name="movieDetail"),
    path("register/", views.register_page, name="startPage"),
    path("postuser/", views.postuser, name="userPost"),
]
