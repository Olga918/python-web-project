import uuid
from django.db import models
from datetime import datetime

def set_no_set(value):
    return value if value != None else "no-set"

class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    name = models.CharField('Назва категорії',max_length=255)
    created_at = models.DateField('Дата створення',default=datetime.now)
    deleted_at = models.DateField('Дата видалення',null=True)
    
    @property
    def Name(self):
        return self.name
    
    # def __str__(self):
    #     return f"""
    # CategoryId: {self.id}
    # Name: {self.name}
    # Created at: {self.created_at}
    # Deleted at: {set_no_set(self.deleted_at)}
    # """
    def __str__(self):
        return self.Name
        
    class Meta:
        db_table = "dj_categories"
        
class Tag(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    name = models.CharField('Тег',max_length=50)
    
    # def __str__(self):
    #     return f"""
    # TagId: {self.id}
    # Name: {self.name}
    # """
    def __str__(self):
        return self.name    

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
   
    name = models.CharField('Назва товару',null=False, max_length=300)
    price = models.FloatField('Ціна', null = False)
    description = models.TextField('Опис товару', null=True)
    image_path = models.URLField('Картинка',null=True, blank=True, max_length=255)
    created_at = models.DateField('Дата створення',default=datetime.now)
    deleted_at = models.DateField('Дата видалення',null=True)
    
    """ Relations """
    
    category = models.ForeignKey(Category, null=True, default=None, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    
    # def __str__(self):
    #     return f"""
    # ProductID: {self.id},
    # Name: {self.name}
    # Price: {self.price}
    # Description: {set_no_set(self.description)}
    # Image URL: {set_no_set(self.image_path)}
    # Created at: {self.created_at}
    # Deleted at: {set_no_set(self.deleted_at)}
    # """
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'dj_products'
        verbose_name = 'Товар'
        constraints = [
            models.CheckConstraint(
                condition = models.Q(price__gt=0),
                name = 'price_gt_zero'
            )
        ]
        permissions = [
            ("my_permission", "Can do something")
        ]
        
