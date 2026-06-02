from django.conf import settings
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва жанру")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва фільму")
    description = models.TextField(verbose_name="Опис фільму")
    release_date = models.DateField(verbose_name="Дата виходу")
    country = models.CharField(max_length=100, verbose_name="Країна")
    poster = models.ImageField(
        upload_to="posters/",
        blank=True,
        null=True,
        verbose_name="Постер",
    )
    rating = models.PositiveSmallIntegerField(
        default=3,
        verbose_name="Рейтинг",
    )
    genres = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="movies",
        verbose_name="Жанри",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-release_date", "-id"]
        verbose_name = "Фільм"
        verbose_name_plural = "Фільми"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name="rating_between_1_and_5",
            ),
        ]

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Фільм",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="movie_reviews",
        verbose_name="Користувач",
    )
    text = models.TextField(verbose_name="Текст відгуку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        permissions = [
            ("can_moderate_reviews", "Може модерувати відгуки"),
        ]

    def __str__(self):
        return f"{self.user}: {self.text[:40]}"
