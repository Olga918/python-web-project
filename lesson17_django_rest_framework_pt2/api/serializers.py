from rest_framework import serializers
from django.contrib.auth import models as auth_models
from .models import Category, Article, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ['id', 'username', 'email']
        
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model= Comment
        fields = ['id', 'author', 'content', 'created_at']
        
class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = serializers.ReadOnlyField(source='category.title')
    
    class Meta:
        model= Article
        fields = ['id', 'title', 'slug', 'author', 'category', 'created_at']
        
class ArticleRetrieveSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model= Article
        fields = ['id', 'title', 'slug', 'author', 'category','comments', 'created_at']
      
      
# Серіалізатор який необхідний для створення нової статті        
class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'content', 'category']
        
        # Виключаємо обов'язкове введення для слагу, ми його створимо на рівні моделі
        extra_kwargs = {
            'slug': {'required': False, 'allow_null': True}
        }