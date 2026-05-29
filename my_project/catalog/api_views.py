from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from catalog.models import Category, Product
from drf_spectacular.utils import extend_schema
from .serializers import CategorySerializer, ProductSerializer

@extend_schema(summary='Список категорий', 
description='Получить список всех категорий',
tags=['Категории'])
class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@extend_schema(summary='Список продуктов', 
description='Получить список всех продуктов',
tags=['Продукты'])
class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@extend_schema(summary='Детали категории',
description='Получить, обновить или удалить категорию по ID',
tags=['Категории'])
class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@extend_schema(summary='Детали продукта',
description='Получить, обновить или удалить продукт по ID',
tags=['Продукты'])
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]