from bangazon_api.models.like import Like
from rest_framework import serializers
from bangazon_api.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'average_rating',
                  'quantity', 'location', 'image_path', 'category', 'store',
                  'ratings', 'number_purchased')
        depth = 1


class CreateProductSerializer(serializers.Serializer):
    categoryId = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(decimal_places=2, max_digits=7)
    description = serializers.CharField()
    quantity = serializers.IntegerField()
    location = serializers.CharField()
    image = serializers.ImageField()


class AddRemoveRecommendationSerializer(serializers.Serializer):
    username = serializers.CharField()


class AddProductRatingSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    review = serializers.CharField()
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'product', 'customer')

class AddLikeSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    customer = serializers.IntegerField()
