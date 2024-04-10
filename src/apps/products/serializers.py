from decimal import Decimal

from rest_framework import serializers

from apps.products.models import Collection, Product, ProductImages, Review


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ("id", "title", "products_count")

    products_count = serializers.IntegerField(read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = ("id", "image", "flag")

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return ProductImages.objects.create(product_id=product_id, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "slug",
            "images",
            "inventory",
            "unit_price",
            "price_with_tax",
            "collection",
        )

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "date", "name", "description")

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "title", "unit_price")
