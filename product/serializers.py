from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    
    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    
    def get_products_count(self, category):
        return category.product_set.count()
    
    
    def validate_name(self,name):
        if len(name)<2:
            raise ValidationError("Название категории должно содержать минимум 2 символа.")
        return name
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, price):
        if price <= 0:
            raise ValidationError("Цена должна быть болше нуля.")
        return price    
 
    def validate_title(self, title):
        if len(title) > 100:
           raise ValidationError("Заголвок слишком длинный! Максимум 100 символов.")
        return title

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars product'.split()
    
    def validate_stars(self, stars):
        if stars is not None and (stars < 1 or stars > 5):
           raise ValidationError("Рейтинг должен быть от 1 до 5.")
        return stars


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