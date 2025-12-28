from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    def get_products_count(self, category):
        return category.product_set.count()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '_all_'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars product'.split()

class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title reviews rating'.split()

    def get_rating(self, product):
        reviews = product.reviews.all()
        if reviews.exists():
            total_stars = sum([review.stars for review in reviews])
            return total_stars / reviews.count()
        return 0