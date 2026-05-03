from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic.base import RedirectView

from core.views import ProductView


def _lesson7_urlconf_ok(_request):
    return HttpResponse("Lesson7 project.urls OK", content_type="text/plain; charset=utf-8")


urlpatterns = [
    path("lesson7-alive/", _lesson7_urlconf_ok),
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),
    # часта помилка: /task/ замість /tasks/
    path("task/", RedirectView.as_view(url="/tasks/", permanent=False)),
    path("core/cbv/", ProductView.as_view(), name="core_product_list_cbv"),
    path("core/cbv", ProductView.as_view()),
    path("core/", include("core.urls")),
    path("", include("core.urls")),
]
