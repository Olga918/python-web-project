from datetime import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .form import MovieForm, UserForm
from .models import Movie


def movie_list(request: HttpRequest):
    movies = Movie.objects.all()
    return render(request, "movies_list.html", {"movies": movies})


def movie_add(request: HttpRequest):
    if request.method == "GET":
        return render(request, "movie_form.html", {"form": MovieForm()})

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            return redirect("movieDetail", pk=movie.pk)
        return render(request, "movie_form.html", {"form": form})

    return HttpResponseNotAllowed(["GET", "POST"])


def movie_detail(request: HttpRequest, pk: int):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, "movie_detail.html", {"movie": movie})


def register_page(request: HttpRequest):
    return render(request, "django-form.html", {"form": UserForm()})


def postuser(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    userform = UserForm(request.POST, request.FILES)
    if userform.is_valid():
        name = userform.cleaned_data["name"]
        surname = userform.cleaned_data["surname"]
        age = userform.cleaned_data["age"]

        picture = userform.cleaned_data.get("picture")
        image_url = None
        if picture:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            file_type = picture.name.rsplit(".", 1)[-1]
            file_name = fs.save(
                f"{datetime.timestamp(datetime.now())}.{file_type}",
                picture,
            )
            image_url = fs.url(file_name)

        return render(
            request,
            "user_page.html",
            {
                "name": name,
                "surname": surname,
                "age": age,
                "imageUrl": image_url,
            },
        )

    return render(request, "django-form.html", {"form": userform})
