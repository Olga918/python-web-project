from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_create, name="eventCreate"),
    path("result/", views.event_result_redirect, name="eventResult"),
    path("result/<int:event_id>/", views.event_detail, name="eventDetail"),
    path("register/", views.index, name="registerPage"),
    path("user/", views.postuser, name="postUser"),
]
