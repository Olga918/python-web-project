from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.http import HttpRequest
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, Tag
from .forms import ProductForm, RegisterForm

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
    

def register_page(request:HttpRequest):
    return render(request, 'register.html', {"form":RegisterForm()})

def register_view(request:HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("auth_page")
        else:
            print(form.errors)
            return redirect("register_page")
        
def login_page(request:HttpRequest):
    if request.user.is_authenticated: return redirect("auth_page")
    return render(request, 'register.html', {"form":AuthenticationForm(), "button":"Sign In", "action":"login_view"})

def login_view(request:HttpRequest):
    if request.method == 'POST':
        print("SUCCESS")
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            print("SUCCESS")
            user = form.get_user()
            login(request, user)
            return redirect("auth_page")
        else:
            print("SUCCES2S")
            print(form.errors)
            return redirect("login_page")
        
def logout_view(request:HttpRequest):
    logout(request)
    return redirect("login_page")

@login_required
def auth_page(request:HttpRequest):
    return render(request, "auth_page.html", {"user":request.user})