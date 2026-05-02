from django.urls import path

from . import views

"""
<str:property_name> - path("person/<str:name>/<str:surname>", views.get_person, name='personPage')
"""

# Домашні завдання: кожне — окремий path тут + нова функція в views.py
# Повний URL: http://127.0.0.1:8000/app/... (див. firstProject.urls — include('core.urls'))
urlpatterns = [
    path('', views.index, name='homePage'),
    path('person/<str:name>/<str:surname>/', views.get_person, name='personPage'),
    path('product/<int:id>/', views.get_product, name='productById'),
    path('request/', views.get_request, name='requestInfo'),
    path('homework/1/', views.homework_datetime, name='homework1'),
    path('homework/2/', views.homework_multiplication, name='homework2'),
    # ДЗ 3: динамічні URL — список, за id, за назвою (slug у шляху)
    path('homework/3/', views.homework_tasks_list, name='homework3'),
    path('homework/3/id/<int:task_id>/', views.homework_task_by_id, name='homework3_task_by_id'),
    path('homework/3/name/<slug:task_slug>/', views.homework_task_by_slug, name='homework3_task_by_slug'),
]