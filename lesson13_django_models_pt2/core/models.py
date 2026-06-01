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
    
    name = models.CharField(max_length=255)
    created_at = models.DateField(default=datetime.now)
    deleted_at = models.DateField(null=True)
    
    @property
    def Name(self):
        return self.name
    
    def __str__(self):
        return f"""
    CategoryId: {self.id}
    Name: {self.name}
    Created at: {self.created_at}
    Deleted at: {set_no_set(self.deleted_at)}
    """
    
    class Meta:
        db_table = "dj_categories"
        
class Tag(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"""
    TagId: {self.id}
    Name: {self.name}
    """
    

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
   
    name = models.CharField(null=False, max_length=300)
    price = models.FloatField(null = False)
    description = models.TextField(null=True)
    image_path = models.URLField(null=True, blank=True, max_length=255)
    created_at = models.DateField(default=datetime.now)
    deleted_at = models.DateField(null=True)
    
    """ Relations """
    
    category = models.ForeignKey(Category, null=True, default=None, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    
    def __str__(self):
        return f"""
    ProductID: {self.id},
    Name: {self.name}
    Price: {self.price}
    Description: {set_no_set(self.description)}
    Image URL: {set_no_set(self.image_path)}
    Created at: {self.created_at}
    Deleted at: {set_no_set(self.deleted_at)}
    """
    
    class Meta:
        db_table = 'dj_products'
        constraints = [
            models.CheckConstraint(
                condition = models.Q(price__gt=0),
                name = 'price_gt_zero'
            )
        ]
        
class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return f"""
    CourseId: {self.id}
    Name: {self.name}
    """
    
class Student(models.Model):
    name = models.CharField(max_length=150)
    course = models.ManyToManyField(Course)
    
    def __str__(self):
        return f"""
    StudentId: {self.id}
    Name: {self.name}
    """

''' Якщо необхідно додати свою інформацію у проміжну таблицю, використовуйте цей спосіб
class Course_test(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return f"""
    CourseId: {self.id}
    Name: {self.name}
    """
    
class Student_test(models.Model):
    name = models.CharField(max_length=150)
    course = models.ManyToManyField(null=True, to=Course_test, through="CourseStudent")
    
    def __str__(self):
        return f"""
    StudentId: {self.id}
    Name: {self.name}
    """

from django.utils.timezone import now
class CourseStudent(models.Model):
    student = models.ForeignKey(Student_test, on_delete=models.CASCADE)
    course = models.ForeignKey(Course_test, on_delete=models.CASCADE)
    created_at = models.DateField(
        default=now
    )
    class Meta:
        db_table="dj_studentxcourse"
    
'''