from django.db import models


class Category(models.Model):
    name = models.CharField('Назва', max_length=200)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Категорія',
    )
    title = models.CharField('Заголовок', max_length=300)
    slug = models.SlugField('Слаг', unique=True)
    # Шлях до файлу всередині wwwroot (для {% static %})
    image = models.CharField(
        'Зображення (шлях у static)',
        max_length=300,
        default='assets/news/politika-biudzhet.jpg',
    )
    teaser = models.CharField('Короткий опис', max_length=500)
    body = models.TextField('Повний текст')
    published_at = models.DateTimeField('Дата публікації', auto_now_add=True)

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['-published_at']

    def __str__(self):
        return self.title
