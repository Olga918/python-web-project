from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from .serializers import ProductSerializer
from .models import Product, products
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

# FBV - Function Based View
def index(request:HttpRequest):
    return HttpResponse("<h1>Home</h1>")

# CBV - Class Based View
class ProductView(View):
    @csrf_exempt
    def put(self, request:HttpRequest):
        return JsonResponse({"message":"POST!!!"})
    
    def get(self, request:HttpRequest):
        param_id = request.GET.get('id', None)
        param_slug = request.GET.get('slug', None)
        
        print(cache.get(request.path.replace('/',''), None, 1))
        
        if param_id == None and param_slug == None:
            if len(products) > 0:
                return JsonResponse(
                    products, encoder=ProductSerializer, safe=False
                )
            else:
                r = JsonResponse({"message": "Products not found"})
                r.status_code = 404
                r.reason_phrase = 'Not Found'
                return r
        
        if param_id is not None:
            try:
                id = int(param_id)
            except ValueError:
                r = JsonResponse({"message":"Id parameter must be number"})
                r.status_code = 400
                r.reason_phrase = 'Bad Request'
                return r
            result = list(filter(lambda x: x.id == id, products))
            if len(result) < 1:
                r = JsonResponse({"message":"Product not found"})
                r.status_code = 404
                r.reason_phrase = 'Not Found'
                return r
            return JsonResponse(
                result[0], encoder=ProductSerializer, safe=False
            )
        elif param_slug is not None:
            result = list(filter(lambda x: x.slug == param_slug, products))
            if len(result) < 1:
                r = JsonResponse({"message":"Product not found"})
                r.status_code = 404
                r.reason_phrase = 'Not Found'
                return r
            return JsonResponse(
                result[0], encoder=ProductSerializer, safe=False
            )
        return JsonResponse({"message": "Bad request"}, status=400)