from django.shortcuts import render
import random
from .models import Product

def seed():
    Product.objects.create(
        name = "product1",
        price = round(random.uniform(100, 1000),2),
        description = "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable.",
        image_path = 'http://eheziskel.lr/mov'
    )
    
    Product.objects.create(
        name = "product2",
        price = round(random.uniform(100, 1000),2),
        description = "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable.",
        image_path = 'http://eheziskel.lr/mov'
    )
    
    Product.objects.create(
        name = "product3",
        price = round(random.uniform(100, 1000),2),
        image_path = 'http://eheziskel.lr/mov'
    )
    
    Product.objects.create(
        name = "product4",
        price = round(random.uniform(100, 1000),2),
    )
    
    Product.objects.create(
        name = "product5",
        price = round(random.uniform(100, 1000),2),
        description = "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable.",
    )
    
    Product.objects.create(
        name = "product6",
        price = round(random.uniform(100, 1000),2),
    )
    
    Product.objects.create(
        name = "product7",
        price = round(random.uniform(100, 1000),2),
        description = "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable.",
        image_path = 'http://eheziskel.lr/mov'
    )
    
def print_product(product):
    if not product:
        print("Product is null")
        return
    print("="*20)
    print(product)
    print("="*20)
    
def print_products(products):
    if not products or len(products)<=0:
        print("No products")
        return
    
    print(f"\n{"-"*20} Start printing {"-"*20}")
    for item in products:
        print_product(item)
    print(f"\n{"-"*20} End printing {"-"*20}")
    

products = Product.objects.all()
# print_products(products)

products = Product.objects.all().order_by("name","-price")
# print_products(products)

# MySQLdb.OperationalError: (3819, "Check constraint 'price_gt_zero' is violated.")
# Product.objects.create(
#         name = "product8",
#         price = -100,
#         description = "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable.",
#         image_path = 'http://eheziskel.lr/mov'
#     )

products = Product.objects.filter(id='04bcef4606fd4a3f97e4569515e0b9a5')
# print_products(products)

"(<,>,<=,>=): lt, gt, lte, gte"
products = Product.objects.filter(price__gte=200).order_by("name")
# print_products(products)

products = Product.objects.filter(price__in=[141.19, 488.91, 200]).order_by("name")
# print_products(products)

products = Product.objects.filter(price__range=(100,300)).order_by("name")
# print_products(products)

products = Product.objects.filter(name__exact='prOduct2').order_by("name")
# print_products(products)

products = Product.objects.filter(name__icontains='PR').order_by("name")
# print_products(products)

products = Product.objects.filter(name__istartswith='PR').order_by("name")
# print_products(products)

products = Product.objects.filter(name__iendswith='cT2').order_by("name")
# print_products(products)

products = Product.objects.filter(name__istartswith='PR') & Product.objects.filter(price__lte=200)
products = products.order_by("name")
# print_products(products)

products = Product.objects.filter(price__lte=150) | Product.objects.filter(price__gte=300)
products = products.order_by("name")
# print_products(products)


# product = Product.objects.get(id="04bcef4606fd4a3f97e4569515e0b9a5")
# print_product(product)

from django.core.exceptions import ObjectDoesNotExist

try:
    product = Product.objects.get(id="fe0e74b4b6e65b008d204d6cf71fe4d6")
    print(product)
except ObjectDoesNotExist:
    print("Product not found")
    
# product = Product.objects.get_or_create(id="fe0e74b4b6e65b008d204d6cf71fe4d6", name="Product8", price=round(random.uniform(100,1000),2))
# print_product(product)

# samsung = Product(name="samsung", price=299.00)
# samsung.save()

# print_product(samsung)

try:
    Product.objects.get(id='4cbc7ddd29f9446fa1f1eebf7e8ad171').delete()
except:
    pass


from django.db.models import F

try:
    pass
    # Product.objects.filter(id='fe0e74b4b6e65b008d204d6cf71fe4d6').update(name="Samsung", price=F("price")+10)
except:
    pass



