from django.db import migrations


def seed(apps, schema_editor):
    Category = apps.get_model('news', 'Category')
    Article = apps.get_model('news', 'Article')

    if Category.objects.exists():
        return

    pol = Category.objects.create(name='Політика', slug='polityka')
    sport = Category.objects.create(name='Спорт', slug='sport')
    tech = Category.objects.create(name='Технології', slug='tehnologii')

    Article.objects.create(
        category=pol,
        title='Ухвалено оновлений проєкт місцевого бюджету',
        slug='miskyi-biudzhet-2026',
        image='assets/firefox.jpg',
        teaser='Коротко про ключові статті витрат і пріоритети на наступний рік.',
        body=(
            'Міська рада підтримала оновлення бюджету з акцентом на освіту, медицину та дороги.\n\n'
            'Деталі фінансування будуть оприлюднені протягом тижня на офіційному порталі.'
        ),
    )
    Article.objects.create(
        category=pol,
        title='Міжнародні партнери представили програму грантів для громад',
        slug='grantly-dlia-hromad',
        image='assets/firefox.jpg',
        teaser='Коментар експертів щодо можливостей участі малих міст та сіл.',
        body=(
            'Програмою передбачено конкурсний відбір інфраструктурних проектів до 150 тис.\n'
            'Дедлайни подачі заяв — у липні-серпні поточного року.'
        ),
    )
    Article.objects.create(
        category=sport,
        title='Команда готується до півфінального матчу',
        slug='pivfinal-match',
        image='assets/firefox.jpg',
        teaser='Головний тренер розповів про стан складу перед грою.',
        body=(
            'Після перемоги в чвертьфіналі команда три дні провела на відновленні.\n\n'
            'Матч відбудеться в суботу о 18:00; квитки — на сайті стадіону.'
        ),
    )
    Article.objects.create(
        category=sport,
        title='Чемпіонат області: підсумки туру',
        slug='chempionat-oblasti-tur',
        image='assets/firefox.jpg',
        teaser='Таблиця лідерів змінилася після нічиї в центральному поєдинку.',
        body=(
            'У центральному матчі туру зафіксовано нічию 1:1. Лідер зберг перевагу в одне очко.\n'
            'Наступний тур через тиждень.'
        ),
    )
    Article.objects.create(
        category=tech,
        title='Відкрито реєстрацію на конференцію з кібербезпеки',
        slug='kiberbezpeka-konferenciia',
        image='assets/firefox.jpg',
        teaser='Програма охоплює хмарну безпеку, Zero Trust та аудит процесів.',
        body=(
            'Онлайн- і офлайн-формати участі.\n'
            'Ключові спікери — практики з держсектора та міжнародні консультанти.'
        ),
    )
    Article.objects.create(
        category=tech,
        title='Нові рекомендації щодо оновлення бібліотек у продакшені',
        slug='olibky-prod-update',
        image='assets/firefox.jpg',
        teaser='Що варто перевірити перед оновленням залежностей у вашому Django-проєкті.',
        body=(
            'Перед оновленням зніміть дамп БД, запустіть тестовий середовище та перевірте CHANGELOG '
            'критичних пакунків.'
        ),
    )


def unseed(apps, schema_editor):
    Category = apps.get_model('news', 'Category')
    Article = apps.get_model('news', 'Article')
    Article.objects.all().delete()
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
