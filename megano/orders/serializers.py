from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from shop.serializers import (
    ImageProductSerializer,
    TagSerializer,
    CategorySerializer,
    ReviewSerializer,
)
from shop.models import Product
from .models import Order


class CartProductsSerializer(serializers.ModelSerializer):

    """Сериализатор товаров в корзине"""

    category = CategorySerializer()
    images = ImageProductSerializer(many=True)
    tags = TagSerializer(many=True)
    count = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    def get_count(self, obj):
        cart = self.context.get("cart")
        if cart:
            return cart.get_quantity(obj)
        order = self.context.get("order")
        product = order.items.get(product_id=obj.id)
        return product.quantity

    def get_rating(self, obj):
        return obj.avg_rating


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    fullName = serializers.CharField(
        source="profile.fullName", allow_null=True, required=False
    )
    email = serializers.EmailField(source="profile.email")
    phone = serializers.CharField(
        max_length=12, source="profile.phone", allow_null=True, required=False
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]

    def get_products(self, obj):
        products_ids = obj.items.values_list("product", flat=True)
        products = Product.objects.filter(pk__in=products_ids)
        serializer = CartProductsSerializer(products, context={"order": obj}, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        profile_data = validated_data.get("profile")
        instance.fullName = profile_data.get("fullName")
        email = profile_data.get("email")
        if not email:
            raise ValidationError("Поле email является обязательным.")
        instance.email = email
        instance.phone = profile_data.get("phone")
        instance.deliveryType = validated_data.get(
            "deliveryType", instance.deliveryType
        )
        instance.paymentType = validated_data.get("paymentType")
        instance.status = validated_data.get("status")
        instance.city = validated_data.get("city")
        instance.address = validated_data.get("address")
        instance.save()
        return instance
