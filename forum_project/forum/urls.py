from django.urls import path

from . import views

app_name = "forum"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_page, name="register"),
    path("signup/", views.register_page, name="signup"),
    path("login/", views.login_page, name="login"),
    path("signin/", views.login_page, name="signin"),
    path("auth/", views.auth_page, name="auth_page"),
    path("logout/", views.logout_view, name="logout"),
    path("category/create/", views.category_create, name="category_create"),
    path("category/<int:pk>/", views.category_detail, name="category_detail"),
    path(
        "category/<int:pk>/delete/",
        views.category_delete,
        name="category_delete",
    ),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("post/<int:pk>/like/", views.post_like_toggle, name="post_like_toggle"),
    path(
        "comment/<int:pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path(
        "comment/<int:pk>/like/",
        views.comment_like_toggle,
        name="comment_like_toggle",
    ),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
]
