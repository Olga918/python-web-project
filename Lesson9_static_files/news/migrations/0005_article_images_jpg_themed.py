from django.db import migrations


# Тематичні JPEG у static (як у класі з firefox.jpg — шлях відносно wwwroot)
SLUG_IMAGES = [
    ('miskyi-biudzhet-2026', 'assets/news/politika-biudzhet.jpg'),
    ('grantly-dlia-hromad', 'assets/news/politika-granty.jpg'),
    ('pivfinal-match', 'assets/news/sport-match.jpg'),
    ('chempionat-oblasti-tur', 'assets/news/sport-tour.jpg'),
    ('kiberbezpeka-konferenciia', 'assets/news/tech-kiber.jpg'),
    ('olibky-prod-update', 'assets/news/tech-dev.jpg'),
]


def forwards(apps, schema_editor):
    Article = apps.get_model('news', 'Article')
    for slug, path in SLUG_IMAGES:
        Article.objects.filter(slug=slug).update(image=path)


def backwards(apps, schema_editor):
    # Старі SVG прибрані з проєкту — відкат шляхів не відновлює файли.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_article_image'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
