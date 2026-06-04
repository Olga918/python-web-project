from rest_framework.pagination import PageNumberPagination

class ArticleListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'pageSize'
    max_page_size = 30