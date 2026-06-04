from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Exists, OuterRef
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from .forms import (
    CategoryForm,
    CommentForm,
    LoginForm,
    PostForm,
    ProfileForm,
    ProfilePasswordForm,
    RegisterForm,
)
from .models import Category, Comment, CommentLike, Post, PostLike


def _redirect_next(request, default_name="forum:auth_page"):
    next_url = request.GET.get("next") or request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect(default_name)


def _posts_queryset(category, user=None):
    qs = category.posts.select_related("author").annotate(
        like_count=Count("likes", distinct=True),
        comment_count=Count("comments", distinct=True),
    )
    if user and user.is_authenticated:
        qs = qs.annotate(
            user_liked=Exists(
                PostLike.objects.filter(post_id=OuterRef("pk"), user_id=user.pk)
            )
        )
    return qs


def _comments_queryset(post, user=None):
    qs = post.comments.select_related("author").annotate(
        like_count=Count("likes", distinct=True),
    )
    if user and user.is_authenticated:
        qs = qs.annotate(
            user_liked=Exists(
                CommentLike.objects.filter(
                    comment_id=OuterRef("pk"), user_id=user.pk
                )
            )
        )
    return qs


def _can_delete_category(user, category):
    return user.is_authenticated and (
        user.is_superuser or category.author_id == user.pk
    )


def _can_delete_post(user, post):
    return user.is_authenticated and (
        user.is_superuser or post.author_id == user.pk
    )


def _can_delete_comment(user, comment):
    return user.is_authenticated and (
        user.is_superuser or comment.author_id == user.pk
    )


def home(request):
    categories = Category.objects.all()
    return render(request, "forum/home.html", {"categories": categories})


@require_http_methods(["GET", "POST"])
def register_page(request):
    if request.user.is_authenticated:
        return _redirect_next(request)

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Вітаємо, {user.nickname}!")
            return _redirect_next(request)
    else:
        form = RegisterForm()

    return render(
        request,
        "forum/register.html",
        {"form": form, "next": request.GET.get("next", "")},
    )


@require_http_methods(["GET", "POST"])
def login_page(request):
    if request.user.is_authenticated:
        return _redirect_next(request)

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.cleaned_data["user"])
            messages.success(request, "Ви успішно увійшли.")
            return _redirect_next(request)
    else:
        form = LoginForm(request)

    return render(
        request,
        "forum/login.html",
        {"form": form, "next": request.GET.get("next", "")},
    )


@login_required
def auth_page(request):
    """Сторінка авторизованого користувача (домашка урок 15)."""
    return render(request, "forum/auth_page.html", {"profile_user": request.user})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "Ви вийшли з облікового запису.")
    return redirect("forum:login")


@require_http_methods(["GET", "POST"])
def category_create(request):
    if not request.user.is_authenticated:
        login_url = reverse("forum:register")
        next_path = request.get_full_path()
        return redirect(f"{login_url}?next={next_path}")

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.author = request.user
            category.save()
            messages.success(request, f"Категорію «{category.name}» створено.")
            return redirect("forum:category_detail", pk=category.pk)
    else:
        form = CategoryForm()

    return render(request, "forum/category_form.html", {"form": form})


@login_required
def profile(request):
    return render(request, "forum/profile.html", {"profile_user": request.user})


@login_required
@require_http_methods(["GET", "POST"])
def profile_edit(request):
    profile_form = ProfileForm(instance=request.user)
    password_form = ProfilePasswordForm(user=request.user)

    if request.method == "POST":
        if "save_profile" in request.POST:
            profile_form = ProfileForm(
                request.POST, request.FILES, instance=request.user
            )
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Профіль оновлено.")
                return redirect("forum:profile")
        elif "change_password" in request.POST:
            password_form = ProfilePasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Пароль змінено.")
                return redirect("forum:profile")

    return render(
        request,
        "forum/profile_edit.html",
        {"profile_form": profile_form, "password_form": password_form},
    )


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = _posts_queryset(category, request.user)
    post_form = PostForm()
    can_delete_category = _can_delete_category(request.user, category)

    if request.method == "POST" and "create_post" in request.POST:
        if not request.user.is_authenticated:
            login_url = reverse("forum:login")
            return redirect(f"{login_url}?next={request.get_full_path()}")
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.category = category
            post.author = request.user
            post.save()
            messages.success(request, "Пост опубліковано.")
            return redirect("forum:category_detail", pk=category.pk)
        messages.error(request, "Не вдалося опублікувати пост. Перевірте текст у полі нижче.")

    return render(
        request,
        "forum/category_detail.html",
        {
            "category": category,
            "posts": posts,
            "post_form": post_form,
            "can_delete_category": can_delete_category,
        },
    )


@require_http_methods(["GET", "POST"])
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if not _can_delete_category(request.user, category):
        return HttpResponseForbidden("Ви не можете видалити цю категорію.")

    if request.method == "POST":
        name = category.name
        category.delete()
        messages.success(request, f"Категорію «{name}» видалено разом із постами та коментарями.")
        return redirect("forum:home")

    return render(
        request,
        "forum/category_confirm_delete.html",
        {"category": category},
    )


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related("category", "author"), pk=pk
    )
    like_count = post.likes.count()
    user_liked_post = False
    if request.user.is_authenticated:
        user_liked_post = PostLike.objects.filter(
            user=request.user, post=post
        ).exists()

    comments = _comments_queryset(post, request.user)
    comment_form = CommentForm()
    can_delete_post = _can_delete_post(request.user, post)

    if request.method == "POST" and "create_comment" in request.POST:
        if not request.user.is_authenticated:
            login_url = reverse("forum:register")
            return redirect(f"{login_url}?next={request.get_full_path()}")
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Коментар додано.")
            return redirect("forum:post_detail", pk=post.pk)

    return render(
        request,
        "forum/post_detail.html",
        {
            "post": post,
            "like_count": like_count,
            "user_liked_post": user_liked_post,
            "comments": comments,
            "comment_form": comment_form,
            "can_delete_post": can_delete_post,
        },
    )


@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not _can_delete_post(request.user, post):
        return HttpResponseForbidden("Ви не можете видалити цей пост.")
    category_pk = post.category_id
    post.delete()
    messages.success(request, "Пост видалено.")
    return redirect("forum:category_detail", pk=category_pk)


@login_required
@require_POST
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if not _can_delete_comment(request.user, comment):
        return HttpResponseForbidden("Ви не можете видалити цей коментар.")
    post_pk = comment.post_id
    comment.delete()
    messages.success(request, "Коментар видалено.")
    return redirect("forum:post_detail", pk=post_pk)


@login_required
@require_POST
def post_like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = PostLike.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("forum:post_detail", pk=pk)


@login_required
@require_POST
def comment_like_toggle(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    like, created = CommentLike.objects.get_or_create(
        user=request.user, comment=comment
    )
    if not created:
        like.delete()
    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("forum:post_detail", pk=comment.post_id)
