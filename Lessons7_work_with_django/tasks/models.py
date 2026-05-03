from django.db import models


class Task(models.Model):
    """Завдання з заголовком, текстом і датами."""

    title = models.CharField("заголовок задачі", max_length=200)
    text = models.TextField("текст задачі")
    start_date = models.DateField("дата початку")
    end_date = models.DateField("дата завершення")

    class Meta:
        ordering = ["-start_date", "id"]
        verbose_name = "завдання"
        verbose_name_plural = "завдання"

    def __str__(self) -> str:
        return self.title
