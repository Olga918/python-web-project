from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Product
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name ='product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.select_related('category').prefetch_related('tags').order_by('name')
    
class ProductCreateView(CreateView):
    model=Product
    form_class=ProductForm
    template_name='product_create.html'
    success_url=reverse_lazy('product-list')