from rest_framework import serializers
from reviews.models import Review
from catalog.models import Product
from django.contrib.auth.models import User

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    product = ProductShortSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'rating', 'user', 'product']