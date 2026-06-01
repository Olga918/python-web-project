from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

from .models import Category, Comment, Post, User


class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(
        required=True,
        label="Дата народження",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-input"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "nickname",
            "email",
            "first_name",
            "last_name",
            "birth_date",
        )
        labels = {
            "first_name": "Ім'я",
            "last_name": "Прізвище",
            "nickname": "Нікнейм",
            "email": "Електронна пошта",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-input"}),
            "last_name": forms.TextInput(attrs={"class": "form-input"}),
            "nickname": forms.TextInput(attrs={"class": "form-input"}),
            "email": forms.EmailInput(attrs={"class": "form-input"}),
        }


class LoginForm(forms.Form):
    nickname = forms.CharField(
        label="Нікнейм",
        widget=forms.TextInput(attrs={"class": "form-input", "autofocus": True}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        nickname = cleaned.get("nickname")
        password = cleaned.get("password")
        if nickname and password and self.request:
            user = authenticate(
                self.request, username=nickname, password=password
            )
            if user is None:
                raise forms.ValidationError("Невірний нікнейм або пароль.")
            cleaned["user"] = user
        return cleaned


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname", "first_name", "last_name", "birth_date", "avatar"]
        labels = {
            "nickname": "Нікнейм",
            "first_name": "Ім'я",
            "last_name": "Прізвище",
            "birth_date": "Дата народження",
            "avatar": "Аватар",
        }
        widgets = {
            "nickname": forms.TextInput(attrs={"class": "form-input"}),
            "first_name": forms.TextInput(attrs={"class": "form-input"}),
            "last_name": forms.TextInput(attrs={"class": "form-input"}),
            "birth_date": forms.DateInput(
                attrs={"type": "date", "class": "form-input"}
            ),
            "avatar": forms.FileInput(attrs={"class": "form-input"}),
        }


class ProfilePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update({"class": "form-input"})
        self.fields["new_password1"].widget.attrs.update({"class": "form-input"})
        self.fields["new_password2"].widget.attrs.update({"class": "form-input"})
        self.fields["old_password"].label = "Поточний пароль"
        self.fields["new_password1"].label = "Новий пароль"
        self.fields["new_password2"].label = "Підтвердження нового пароля"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "image"]
        labels = {
            "name": "Назва категорії",
            "description": "Опис",
            "image": "Іконка категорії (рекомендовано — різне фото для кожної теми)",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(
                attrs={"class": "form-input form-textarea", "rows": 4}
            ),
            "image": forms.FileInput(attrs={"class": "form-input"}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]
        labels = {"text": "Текст поста"}
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-input form-textarea",
                    "rows": 5,
                    "placeholder": "Напишіть текст поста тут…",
                    "required": True,
                }
            ),
        }

    def clean_text(self):
        text = (self.cleaned_data.get("text") or "").strip()
        if not text:
            raise forms.ValidationError("Введіть текст поста.")
        return text


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "Ваш коментар"}
        widgets = {
            "text": forms.Textarea(
                attrs={"class": "form-input form-textarea", "rows": 3, "placeholder": "Напишіть коментар…"}
            ),
        }
