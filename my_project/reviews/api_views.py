from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Review
from .serializers import ReviewSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(summary='Список отзывов', 
description='Получить список всех отзывов или создать новый отзыв',
tags=['Отзывы'])
class ReviewListAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(summary='Детали отзыва', 
description='Получить, обновить или удалить отзыв по ID',
tags=['Отзывы'])
class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_update(self, serializer):
        # Allow only the author to update their review
        if serializer.instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы можете редактировать только свои отзывы")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Allow only the author to delete their review
        if instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы можете удалять только свои отзывы")
        instance.delete()