from datetime import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .form import MovieForm, UserForm
from .models import Movie

SORT_OPTIONS = {
    "rating": "rating",
    "title": "title",
    "release_date": "-release_date",
}


def movie_list(request: HttpRequest):
    sort = request.GET.get("sort", "release_date")
    order_by = SORT_OPTIONS.get(sort, "-release_date")
    movies = Movie.objects.all().order_by(order_by)
    return render(
        request,
        "movies_list.html",
        {"movies": movies, "current_sort": sort},
    )


def movie_add(request: HttpRequest):
    if request.method == "GET":
        return render(
            request,
            "movie_form.html",
            {"form": MovieForm(), "form_title": "Новий фільм"},
        )

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            return redirect("movieDetail", pk=movie.pk)
        return render(
            request,
            "movie_form.html",
            {"form": form, "form_title": "Новий фільм"},
        )

    return HttpResponseNotAllowed(["GET", "POST"])


def movie_edit(request: HttpRequest, pk: int):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "GET":
        return render(
            request,
            "movie_form.html",
            {
                "form": MovieForm(instance=movie),
                "form_title": "Редагувати фільм",
                "movie": movie,
            },
        )

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save()
            return redirect("movieDetail", pk=movie.pk)
        return render(
            request,
            "movie_form.html",
            {"form": form, "form_title": "Редагувати фільм", "movie": movie},
        )

    return HttpResponseNotAllowed(["GET", "POST"])


def movie_delete(request: HttpRequest, pk: int):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "GET":
        return render(request, "movie_delete.html", {"movie": movie})

    if request.method == "POST":
        movie.delete()
        return redirect("movieList")

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
