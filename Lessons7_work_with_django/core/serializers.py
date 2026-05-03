from django.core.serializers.json import DjangoJSONEncoder

from .models import Product


class ProductSerializer(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Product):
            return {
                "id": obj.id,
                "slug": obj.slug,
                "name": obj.name,
                "description": obj.description,
            }
        return super().default(obj)
