from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import Genre, Movie, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ("user", "text", "created_at")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "movie_count")
    search_fields = ("name",)
    ordering = ("name",)

    @admin.display(description="Фільмів")
    def movie_count(self, obj):
        return obj.movies.count()


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "rating",
        "country",
        "release_date",
        "review_count",
        "genre_list",
    )
    list_filter = ("country", "rating", "genres", "release_date")
    search_fields = ("title", "country", "description")
    ordering = ("-release_date", "-id")
    filter_horizontal = ("genres",)
    inlines = [ReviewInline]

    @admin.display(description="Відгуків")
    def review_count(self, obj):
        return obj.reviews.count()

    @admin.display(description="Жанри")
    def genre_list(self, obj):
        return ", ".join(g.name for g in obj.genres.all()) or "—"

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Перегляд фільмів для autocomplete/вибору у відгуках (модератор)."""
        if request.user.is_superuser:
            return True
        if request.user.has_perm("core.can_moderate_reviews"):
            return True
        return super().has_view_permission(request, obj)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user_display", "text_preview", "movie", "created_at")
    list_filter = (("created_at", DateFieldListFilter), "movie")
    search_fields = ("text", "user__username", "movie__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    @admin.display(description="Користувач", ordering="user__username")
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username

    @admin.display(description="Текст відгуку")
    def text_preview(self, obj):
        return obj.text[:80] + ("…" if len(obj.text) > 80 else "")

    def _can_moderate(self, request):
        return request.user.is_superuser or request.user.has_perm(
            "core.can_moderate_reviews"
        )

    def has_module_permission(self, request):
        return self._can_moderate(request)

    def has_view_permission(self, request, obj=None):
        return self._can_moderate(request)

    def has_add_permission(self, request):
        return self._can_moderate(request)

    def has_change_permission(self, request, obj=None):
        return self._can_moderate(request)

    def has_delete_permission(self, request, obj=None):
        return self._can_moderate(request)
