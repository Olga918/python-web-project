from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, CommentLike, Post, PostLike, User


@admin.register(User)
class ForumUserAdmin(UserAdmin):
    list_display = ("nickname", "email", "first_name", "last_name", "is_staff")
    search_fields = ("nickname", "email", "first_name", "last_name")
    ordering = ("nickname",)
    fieldsets = (
        (None, {"fields": ("nickname", "password")}),
        ("Особисті дані", {"fields": ("first_name", "last_name", "email", "birth_date", "avatar")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Дати", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "nickname",
                    "email",
                    "first_name",
                    "last_name",
                    "birth_date",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "created_at")
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("category", "author", "created_at")
    list_filter = ("category",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "created_at")
