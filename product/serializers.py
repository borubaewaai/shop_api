from rest_framework import serializers
from .models import Category, Product, Review

class CategoryWithCountSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name product_count'.split()
    def get_products_count(self, category):
        return category.products.count()

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title price category'.split()
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewInProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewInProductSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title price reviews rating'.split()

    def get_rating(self, product):
        reviews = product.reviews.all()
        if not reviews:
            return None
        return round(sum(r.stars for r in reviews)/len(reviews),2)
