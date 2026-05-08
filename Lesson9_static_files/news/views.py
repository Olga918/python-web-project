from django.shortcuts import get_object_or_404, render

from .models import Article, Category


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'news/home.html', {'categories': categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.all()
    return render(
        request,
        'news/category.html',
        {'category': category, 'articles': articles},
    )


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'news/article.html', {'article': article})
