import uuid
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime


def set_no_set(value):
    return value if value != None else "no-set"

class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    

class MyUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True, verbose_name="Електронна пошта")
    first_name = models.CharField(max_length=255, verbose_name="Ім'я")    
    last_name = models.CharField(max_length=255, verbose_name="Прізвище")
    is_active = models.BooleanField(default=True, verbose_name="Бан", help_text="Чи може користувач, користуватися ресурсом") 
    is_staff = models.BooleanField(default=False, verbose_name="Працівник", help_text="Чи є користувач працівником")
    birth_date = models.DateField(null=True, verbose_name="Дата народження")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = MyUserManager()
    
    def __str__(self):
        return self.email   



#region Client site models

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
        

#endregion Client site models