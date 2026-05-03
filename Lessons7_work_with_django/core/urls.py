from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="homePage"),
    path("cbv/", views.ProductView.as_view(), name="product_list_cbv"),
    path("cbv", views.ProductView.as_view()),
]
