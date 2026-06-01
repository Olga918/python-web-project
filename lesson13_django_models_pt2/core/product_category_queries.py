from django.shortcuts import render
import random
from django.db.models import Avg, Max, Min, Sum, Count
from .models import Product, Category
from .product_queries import print_product, print_products


def category_seed():
    Category(name="Smartphones").save()
    Category(name="Laptops").save()
    Category(name="Clothes").save()
    Category(name="Food").save()
    Category(name="Toys").save()
    
# category_seed()
smartphones, result = Category.objects.get_or_create(name="Smartphones")
print(smartphones)

product = Product.objects.get(id="fe0e74b4b6e65b008d204d6cf71fe4d6")
print(product)

product.category = smartphones
# product.save()

products = Product.objects.filter(category__id=smartphones.id)
print_products(products)

products = Product.objects.filter(category__name=smartphones.name)
print_products(products)

# modelInstance.relationModel_set_function

print("Count of products in 'Smartphones'->", smartphones.product_set.count())

product:Product = smartphones.product_set.first()
print_product(product)

def create_products(products_q:int=5):
    list_of_products = []
    for i in range(products_q):
        product = Product(
            name=f"Tovar{i+1}",
            price=round(random.uniform(100,1000),2))
        product.save()
        list_of_products.append(product)
    
    return list_of_products
        
laptops, result = Category.objects.get_or_create(name="Laptops")
# laptops.product_set.add(*create_products())
# laptops.delete()

# laptops.product_set.clear()

print(laptops.product_set.aggregate(Avg('price')))
print(laptops.product_set.aggregate(
    average_price=Avg('price'),
    max_price=Max('price'),
    min_price=Min('price'),
    full_price=Sum('price'),
    product_count=Count('id')
    ))

categories = Category.objects.annotate(
    product_count=Count('product'),
    expensive_product=Max('product__price')
)

for category in categories:
    print("-"*20)
    print(f"Category: '{category.name}'")
    print(f"Product quantity: '{category.product_count}'")
    print(f"Expensive product: '{category.expensive_product}'")
    print("-"*20)




