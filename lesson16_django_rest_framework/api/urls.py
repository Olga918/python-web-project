from rest_framework.routers import DefaultRouter

from django.urls import path, include

from . import views

router = DefaultRouter()
router.register("tasks", viewset=views.TaskViewSet, basename="tasks_view_set")
router.register("products", viewset=views.ProductViewSet, basename="products_view_set")

urlpatterns = [
    path('', include(router.urls)),
    path('simple/', views.SimpleAPI.as_view(), name="simple_view"),
    path('product/', views.ProductListView.as_view(), name="product_list_view"),
    path('product/<uuid:id>', views.ProductView.as_view(), name="product_view"),
]
