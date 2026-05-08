from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='mainPage'),
    path('contacts/', views.contactsPage, name='contactsPage'),
    path('tw/', views.tailwind, name='tailwind'),
]
