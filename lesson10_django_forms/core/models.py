from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва заходу")
    date = models.DateField(verbose_name="Дата заходу")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class Participant(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="participants",
    )
    email = models.EmailField(verbose_name="Email учасника")

    def __str__(self):
        return self.email
