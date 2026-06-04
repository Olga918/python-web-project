from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from django.core.exceptions import ObjectDoesNotExist

from .serializers import ProductSerializer, ProductModelSerializer
from .models import Product

'''
APIView
    def get
    def post
    def put
    def patch
    def delete
'''

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [AllowAny]
    
    # list - сюди приходять запити саме до вибірки, і в цьому методі ми можемо створити якийсь механізм, нарпиклад власна обробка
    # retrieve - сюди приходять запити до конкректного екземпляру, і в цьому методі ми можемо створити якийсь механізм, нарпиклад власна обробка
    
    def list(self, request, *args, **kwargs):
        print(request)
        return super().list(request, *args, **kwargs)

class ProductView(APIView):
    def get(self, request:Request, id):
        try:
            product = Product.objects.get(id=id)
            return Response({
                "status": status.HTTP_200_OK,
                "message":"Ok",
                "data": ProductSerializer(product).data
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message":"Product not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request: Request, id):
        try:
            product = Product.objects.get(id=id)
            updated = ProductSerializer(product, data=request.data)
            if updated.is_valid(raise_exception=True):
                updated.save()
                return Response({
                    "status": status.HTTP_200_OK,
                    "message":"Ok",
                    "data": updated.data
                }, status=status.HTTP_200_OK)
            return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message":"Bad Request",
                    "data": updated.data
                }, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message":"Product not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

class ProductListView(APIView):
    def get(self, request:Request):
        print("query:", request.query_params)
        products = Product.objects.all()
        order = request.query_params.get("order", None)
        if order:
            products = products.order_by("-price" if 'asc' in order[0] else "price")
        return Response({
            "status": status.HTTP_200_OK,
            "message":"Ok",
            "data": ProductSerializer(products, many=True).data
        }, status=status.HTTP_200_OK)
        
    def post(self, request: Request):
        try:
            new_product = ProductSerializer(data=request.data)
            if new_product.is_valid(raise_exception=True):
                new_product.save()
                return Response({
                    "status": status.HTTP_201_CREATED,
                    "message":"Created",
                    "data": new_product.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message":"Bad Request",
                    "data": new_product.data
                }, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message":"Product not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)


class SimpleAPI(APIView):
    def get(self, request:Request):
        return Response({"message":"Welcome to Django REST framework"}, status=status.HTTP_200_OK)
    
    def post(self, request:Request):
        print("Content-Type: ", request.content_type)
        print("POST: ", request.POST)
        print("Body: ", request.data)
        
        r = Response()
        
        data = {
            "status": status.HTTP_200_OK,
            "message": "Ok",
            "data": request.data
        }
        
        r.data = data
        r.headers["Content-Type"] = request.content_type
        if request.data:
            if request.data.get('name', None):
                r.headers["name"] = request.data['name']
        
        # r.status_code = status.HTTP_200_OK
        
        return r
        # return Response({}, status=status.HTTP_200_OK)
