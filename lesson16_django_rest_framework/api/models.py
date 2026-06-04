from django.db import models

import uuid

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField(null=True,blank=True)

    class Meta:
        db_table = "api_products"