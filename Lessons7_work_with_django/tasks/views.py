from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .models import Task


@require_GET
def task_list(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})


@require_http_methods(["GET", "POST"])
def task_add(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        text = (request.POST.get("text") or "").strip()
        start_raw = request.POST.get("start_date")
        end_raw = request.POST.get("end_date")
        if not title or not text or not start_raw or not end_raw:
            return render(
                request,
                "tasks/task_add.html",
                {
                    "error": "Заповніть усі поля.",
                    "title": title,
                    "text": text,
                    "start_date": start_raw or "",
                    "end_date": end_raw or "",
                },
                status=400,
            )
        Task.objects.create(
            title=title,
            text=text,
            start_date=start_raw,
            end_date=end_raw,
        )
        return redirect("task_list")
    return render(request, "tasks/task_add.html", {})


@require_GET
def task_delete(request: HttpRequest, id: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=id)
    task.delete()
    return redirect("task_list")
