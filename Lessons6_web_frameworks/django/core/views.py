from zoneinfo import ZoneInfo

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import escape

from .models import get_task_by_id, get_task_by_slug, products, TASKS

def index(request: HttpRequest):
    return HttpResponse("<h1 style='color:blue'>Hello, Django!</h1>")

def get_person(request: HttpRequest, name: str, surname: str):
    return HttpResponse(f"<h1 style='color:blue'>Hello, {name} {surname}!</h1>")

def get_product(request: HttpRequest, id: int):
    if id < 0 or id >= len(products):
        return HttpResponse("<h1 style='color:red'>Product not found</h1>")
    return HttpResponse(str(products[id]))

def get_request(request: HttpRequest):
    get_items = "".join(
        f"<li>{escape(k)}: {escape(v)}</li>"
        for k, v in request.GET.items()
    )
    body = f"""<ul>
<li>Host: {escape(request.get_host())}</li>
<li>Port: {escape(str(request.get_port()))}</li>
<li>Path: {escape(request.path)}</li>
<li>Path info: {escape(request.path_info)}</li>
<li>GET:
<ul>
{get_items}
</ul>
</li>
</ul>"""
    return HttpResponse(body)





def homework_tasks_list(request: HttpRequest):
    """ДЗ завдання 3: список задач + посилання з динамічними URL."""
    return render(request, "core/homework_tasks_list.html", {"tasks": TASKS})


def homework_task_by_id(request: HttpRequest, task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise Http404("Задачу за таким id не знайдено")
    return render(request, "core/homework_task_detail.html", {"task": task, "found_by": "id"})


def homework_task_by_slug(request: HttpRequest, task_slug: str):
    task = get_task_by_slug(task_slug)
    if task is None:
        raise Http404("Задачу за такою назвою (slug) не знайдено")
    return render(request, "core/homework_task_detail.html", {"task": task, "found_by": "slug"})


def homework_datetime(request: HttpRequest):
    """ДЗ завдання 1: точна дата й час (розмітка в шаблоні, не в Python)."""
    now_utc = timezone.now()
    now_kyiv = timezone.localtime(now_utc, ZoneInfo("Europe/Kyiv"))
    return render(
        request,
        "core/homework_datetime.html",
        {
            "now_utc_iso": now_utc.isoformat(),
            "now_kyiv_display": now_kyiv.strftime("%d.%m.%Y %H:%M:%S"),
            "now_kyiv_iso": now_kyiv.isoformat(timespec="microseconds"),
        },
    )


def homework_multiplication(request: HttpRequest):
    """ДЗ завдання 2: таблиця множення від 1 до 10."""
    n = 10
    rows = [[i * j for j in range(1, n + 1)] for i in range(1, n + 1)]
    return render(
        request,
        "core/homework_multiplication.html",
        {"nums": list(range(1, n + 1)), "rows": rows},
  
  
    )


def homework_tasks_list(request: HttpRequest):
    """ДЗ завдання 3: список задач + посилання з динамічними URL."""
    return render(request, "core/homework_tasks_list.html", {"tasks": TASKS})


def homework_task_by_id(request: HttpRequest, task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise Http404("Задачу за таким id не знайдено")
    return render(request, "core/homework_task_detail.html", {"task": task, "found_by": "id"})


def homework_task_by_slug(request: HttpRequest, task_slug: str):
    task = get_task_by_slug(task_slug)
    if task is None:
        raise Http404("Задачу за такою назвою (slug) не знайдено")
    return render(request, "core/homework_task_detail.html", {"task": task, "found_by": "slug"})
