from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.category_list, name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('article/<slug:slug>/', views.article_detail, name='article'),
]
