from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse

from . import forms
from .models import Event, Participant


def event_create(request: HttpRequest):
    if request.method == "GET":
        return render(
            request,
            "event_form.html",
            {
                "event_form": forms.EventForm(),
                "formset": forms.ParticipantFormSet(prefix="participants"),
            },
        )

    if request.method == "POST":
        event_form = forms.EventForm(request.POST)
        formset = forms.ParticipantFormSet(request.POST, prefix="participants")

        if event_form.is_valid() and formset.is_valid():
            event = Event.objects.create(
                title=event_form.cleaned_data["title"],
                date=event_form.cleaned_data["date"],
            )
            for form in formset:
                email = form.cleaned_data.get("email")
                if email:
                    Participant.objects.create(event=event, email=email)

            return redirect("eventDetail", event_id=event.pk)

        return render(
            request,
            "event_form.html",
            {
                "event_form": event_form,
                "formset": formset,
            },
        )

    return HttpResponse("Method not allowed", status=405)


def event_result_redirect(request: HttpRequest):
    """Якщо відкрити /core/result/ без id — показати останній створений захід."""
    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)

    event = Event.objects.order_by("-id").first()
    if event:
        return redirect("eventDetail", event_id=event.pk)
    return redirect("eventCreate")


def event_detail(request: HttpRequest, event_id: int):
    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)

    event = get_object_or_404(
        Event.objects.prefetch_related("participants"),
        pk=event_id,
    )
    return render(request, "event_detail.html", {"event": event})


def index(request: HttpRequest):
    if request.method == "GET":
        return render(request, "django_form.html", {"form": forms.UserForm()})
    return HttpResponse("Method not allowed", status=405)


def postuser(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.getlist("name_field", None)
        surname = request.POST.get("surname_field", None)

        if len(name) <= 0 or len(surname) <= 0:
            return render(
                request,
                "user_page.html",
                {"error_message": "All fields required"},
            )

        return render(
            request,
            "user_page.html",
            {
                "name": name[0],
                "surname": surname,
            },
        )

    return HttpResponse("Method not allowed", status=405)
