from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from forum.models import Category

# Зображення в forum/static/forum/images/categories/
CATEGORY_IMAGES = {
    "Технології": "technologies.jpg",
    "Ігри": "games.jpg",
    "Навчання": "learning.jpg",
}


class Command(BaseCommand):
    help = "Прив'язує різні іконки до категорій за назвою."

    def handle(self, *args, **options):
        images_dir = (
            Path(__file__).resolve().parent.parent.parent
            / "static"
            / "forum"
            / "images"
            / "categories"
        )
        if not images_dir.is_dir():
            self.stderr.write(self.style.ERROR(f"Папка не знайдена: {images_dir}"))
            return

        updated = 0
        for category in Category.objects.all():
            filename = CATEGORY_IMAGES.get(category.name)
            if not filename:
                self.stdout.write(f"  пропуск: «{category.name}» (немає в мапінгу)")
                continue
            path = images_dir / filename
            if not path.is_file():
                self.stderr.write(self.style.ERROR(f"  файл не знайдено: {path}"))
                continue
            with path.open("rb") as f:
                category.image.save(filename, File(f), save=True)
            updated += 1
            self.stdout.write(self.style.SUCCESS(f"  ✓ {category.name} → {filename}"))

        self.stdout.write(self.style.SUCCESS(f"Готово: оновлено {updated} категорій."))
