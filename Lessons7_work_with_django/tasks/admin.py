from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date")
    list_filter = ("start_date", "end_date")
    search_fields = ("title", "text")
