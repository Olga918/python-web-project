from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "rating", "country", "release_date")
    search_fields = ("title", "country")
