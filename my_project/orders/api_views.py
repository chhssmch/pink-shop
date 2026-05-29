from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from .serializers import OrderSerializer, OrderItemSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(summary='Список заказов', 
description='Получить список всех заказов пользователя',
tags=['Заказы'])
class OrderListAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

@extend_schema(summary='Детали заказа', 
description='Получить, обновить или удалить заказ по ID',
tags=['Заказы'])
class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

@extend_schema(summary='Позиции заказа',
description='Получить список позиций заказа',
tags=['Позиции заказа'])
class OrderItemListAPIView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        return OrderItem.objects.filter(order_id=order_id, order__user=self.request.user)

@extend_schema(summary='Детали позиции заказа',
description='Получить, обновить или удалить позицию заказа',
tags=['Позиции заказа'])
class OrderItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        return OrderItem.objects.filter(order_id=order_id, order__user=self.request.user)