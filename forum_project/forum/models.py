from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Перший аргумент username — значення nickname (так очікує Django)."""

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Нікнейм обов'язковий")
        if not email:
            raise ValueError("Email обов'язковий")
        email = self.normalize_email(email)
        user = self.model(nickname=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """Користувач форуму: вхід за nickname."""

    username = None
    nickname = models.CharField(max_length=50, unique=True, verbose_name="Нікнейм")
    email = models.EmailField(unique=True, verbose_name="Електронна пошта")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата народження")
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )

    USERNAME_FIELD = "nickname"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return self.nickname


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        verbose_name="Іконка",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="categories",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Категорія",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    text = models.TextField(verbose_name="Текст поста")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author}: {self.text[:50]}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField(verbose_name="Текст коментаря")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author}: {self.text[:40]}"


class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_likes",
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["user", "post"]]


class CommentLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_likes",
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["user", "comment"]]
