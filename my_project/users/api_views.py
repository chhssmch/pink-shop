from rest_framework import generics, permissions
from users.models import Profile
from .serializers import ProfileSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(summary='Мой профиль', 
description='Получить и обновить мой профиль',
tags=['Профиль'])
class MyProfileAPIView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.get_or_create(user=self.request.user)[0]