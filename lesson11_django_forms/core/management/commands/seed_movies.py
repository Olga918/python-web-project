from datetime import date

from django.core.management.base import BaseCommand

from core.models import Movie


MOVIES = [
    {
        "title": "Матриця",
        "description": "Хакер Нео дізнається, що світ — симуляція.",
        "release_date": date(1999, 3, 31),
        "country": "США",
        "rating": 5,
        "poster": "posters/1_Matrix.jpg",
    },
    {
        "title": "Титанік",
        "description": "Історія кохання на лайнері, що зіткнувся з айсбергом.",
        "release_date": date(1997, 12, 19),
        "country": "США",
        "rating": 4,
        "poster": "posters/2_Титанік.jpg",
    },
    {
        "title": "Інтерстеллар",
        "description": "Подорож через червоточину, щоб врятувати людство.",
        "release_date": date(2014, 11, 6),
        "country": "США",
        "rating": 5,
        "poster": "posters/4_Інтерстеллар.jpg",
    },
    {
        "title": "Паразити",
        "description": "Родина з бідного кварталу працює в багатому домі.",
        "release_date": date(2019, 5, 30),
        "country": "Південна Корея",
        "rating": 5,
        "poster": "posters/5_Паразити.png",
    },
    {
        "title": "Дюна",
        "description": "Пол Атрейдес на пустельній планеті Арракіс.",
        "release_date": date(2021, 10, 21),
        "country": "США",
        "rating": 4,
        "poster": "posters/6_Дюна.jpg",
    },
    {
        "title": "Зелена миля",
        "description": "Охоронець в'язниці зустрічає ув'язненого з даром зцілення.",
        "release_date": date(1999, 12, 10),
        "country": "США",
        "rating": 5,
        "poster": "posters/7_Зелена_миля.jpg",
    },
]


class Command(BaseCommand):
    help = "Відновити 6 демо-фільмів (після нової міграції)"

    def handle(self, *args, **options):
        if Movie.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"У базі вже є {Movie.objects.count()} фільм(ів). "
                    "Команда не додає дублікати. Видаліть записи або очистіть db.sqlite3."
                )
            )
            return

        for data in MOVIES:
            Movie.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(f"Додано {len(MOVIES)} фільмів."))
