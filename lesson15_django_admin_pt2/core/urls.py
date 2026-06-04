from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('signup/', views.register_page, name="register_page"),
    path('newuser/', views.register_view, name="new_user"),
    path('auth/', views.auth_page, name="auth_page"),
    path('signin/', views.login_page, name="login_page"),
    path('signin-view/', views.login_view, name="login_view"),
    path('logout/', views.logout, name="logout"),
]
