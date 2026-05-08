from django.db import migrations


SLUG_IMAGES = [
    ('miskyi-biudzhet-2026', 'assets/news/ill-01.svg'),
    ('grantly-dlia-hromad', 'assets/news/ill-02.svg'),
    ('pivfinal-match', 'assets/news/ill-03.svg'),
    ('chempionat-oblasti-tur', 'assets/news/ill-04.svg'),
    ('kiberbezpeka-konferenciia', 'assets/news/ill-05.svg'),
    ('olibky-prod-update', 'assets/news/ill-06.svg'),
]


def set_images(apps, schema_editor):
    Article = apps.get_model('news', 'Article')
    for slug, path in SLUG_IMAGES:
        Article.objects.filter(slug=slug).update(image=path)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_seed_demo_news'),
    ]

    operations = [
        migrations.RunPython(set_images, noop_reverse),
    ]
