import uuid
from django.db import models
from datetime import datetime

def set_no_set(value):
    return value if value != None else "no-set"

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