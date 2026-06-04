from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from django.core.exceptions import ObjectDoesNotExist

from .models import Article
from .serializers import ArticleListSerializer, ArticleRetrieveSerializer, ArticleCreateUpdateSerializer
from .paginations import ArticleListPagination

#! ТИМЧАСОВЕ РІШЕННЯ: тільки для тестів поки немає повної роботи з користувачами
class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Custom session authentication that bypasses CSRF validation.
    """
    def enforce_csrf(self, request):
        return  # Do nothing to skip CSRF checking

class ArticleViewSet(viewsets.ModelViewSet):
    #! ТИМЧАСОВЕ РІШЕННЯ: тільки для тестів поки немає повної роботи з користувачами
    authentication_classes = (CsrfExemptSessionAuthentication, )
    
    pagination_class = ArticleListPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    
    filterset_fields = ['category__slug', 'author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    
    def get_queryset(self):
        query = Article.objects.all()
        
        if self.action == 'list':
            return query.select_related('author', 'category')
        if self.action == 'retrieve':
            return query.select_related('author', 'category').prefetch_related('comments__author')
        
        return query
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        # Для методів у яких ми створюємо або видаляємо або оновлюємо використовуємо новий серіалізатор
        if self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateUpdateSerializer
        return ArticleRetrieveSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
