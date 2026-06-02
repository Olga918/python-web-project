from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from core.models import Movie, Review


class Command(BaseCommand):
    help = 'Створює групу "Модератори" з правом can_moderate_reviews.'

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default="moderator",
            help="Нікнейм користувача-модератора (створить, якщо немає)",
        )
        parser.add_argument(
            "--password",
            default="moderator123",
            help="Пароль для нового модератора",
        )

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Модератори")
        if created:
            self.stdout.write(self.style.SUCCESS("Group Moderators created."))
        else:
            self.stdout.write("Group Moderators already exists.")

        ct_review = ContentType.objects.get_for_model(Review)
        for codename in (
            "can_moderate_reviews",
            "view_review",
            "add_review",
            "change_review",
            "delete_review",
        ):
            perm = Permission.objects.get(codename=codename, content_type=ct_review)
            group.permissions.add(perm)

        ct_movie = ContentType.objects.get_for_model(Movie)
        view_movie = Permission.objects.get(codename="view_movie", content_type=ct_movie)
        group.permissions.add(view_movie)

        from django.contrib.auth.models import User as AuthUser

        ct_user = ContentType.objects.get_for_model(AuthUser)
        view_user = Permission.objects.get(codename="view_user", content_type=ct_user)
        group.permissions.add(view_user)

        username = options["username"]
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={"email": f"{username}@example.com"},
        )
        if user_created:
            user.set_password(options["password"])
            user.is_staff = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'User "{username}" created, password: {options["password"]}'
                )
            )
        else:
            user.is_staff = True
            user.save()
            self.stdout.write(f'User "{username}" exists, added to group.')

        user.groups.add(group)
        self.stdout.write(
            self.style.SUCCESS(
                f'"{username}" is in Moderators group (reviews only).'
            )
        )
