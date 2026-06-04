from django.db import models
from django.contrib.auth import models as auth_models

from slugify import slugify

import uuid

class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default = uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) # title: CPP community -> cpp-community
    def __str__(self):
        return f"#{self.id}->{self.title}"
    
    def save(self, *args, **kwargs):
        # TODO: обробити ситуацію якщо назва категорії буде повторюватись
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'api_categories'
    
class Article(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default = uuid.uuid4,
        editable=False
    )
    slug = models.SlugField(unique=True, null=True, blank=True) # title: How to center div -> how-to-center-div
    title = models.CharField(max_length=255)
    content = models.TextField() 
    category = models.ForeignKey(Category, related_name='articles', on_delete=models.PROTECT)
    author = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # TODO: обробити ситуацію якщо назва статті буде повторюватись
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"#{self.id}->{self.slug}"
    
    class Meta:
        db_table = 'api_articles'
        
class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default = uuid.uuid4,
        editable=False
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"#{self.id}"
    
    class Meta:
        db_table = 'api_comments'