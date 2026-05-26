from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-release_date", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name="rating_between_1_and_5",
            ),
        ]

    def __str__(self):
        return self.title
