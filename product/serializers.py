from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, category):
        return category.product_set.count()

    def validate_name(self, name):
        if len(name) < 2:
            raise ValidationError("Название категории должно быть длиннее 2 символов.")
        return name



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

    def validate_stars(self, stars):
        if stars < 1 or stars > 5:
            raise ValidationError("Рейтинг должен быть от 1 до 5.")
        return stars


# --- ТОВАРЫ ---
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

    def validate_price(self, price):
        if price <= 0:
            raise ValidationError("Цена должна быть положительным числом.")
        return price


class ProductReviewSerializer(serializers.ModelSerializer):
  
    reviews = ReviewSerializer(many=True, read_only=True)

    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'reviews', 'average_rating']

    def get_average_rating(self, product):
        reviews = product.reviews.all()
        if reviews.exists():
            return sum([r.stars for r in reviews]) / reviews.count()
        return 0