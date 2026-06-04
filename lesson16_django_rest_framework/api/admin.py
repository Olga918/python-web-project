from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "deadline", "is_completed", "created_at")
    list_filter = ("is_completed",)
    search_fields = ("title",)
