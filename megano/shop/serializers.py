from rest_framework import serializers
from .models import (
    ImageCategory,
    Category,
    ImageProduct,
    Product,
    Review,
    Tag,
    Specification,
    Sale,
)


class ImageCategorySerializer(serializers.ModelSerializer):

    """Сериализатор изображений категорий"""

    class Meta:
        model = ImageCategory
        fields = ["src", "alt"]


class SubcategorySerializer(serializers.ModelSerializer):

    """Сериализатор подкатегорий"""

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        image_obj = obj.image.get()
        return ImageCategorySerializer(image_obj).data

    class Meta:
        model = Category
        fields = ["id", "title", "image"]


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий товаров

    """

    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    def get_image(self, obj):
        image_obj = obj.image.first()
        return ImageCategorySerializer(image_obj).data

    def get_subcategories(self, obj):
        queryset = obj.subcategories.all()
        return SubcategorySerializer(queryset, many=True).data

    class Meta:
        model = Category
        fields = ["id", "title", "image", "subcategories"]


class ImageProductSerializer(serializers.ModelSerializer):

    """Сериализатор Изображения товара"""

    src = serializers.SerializerMethodField()

    class Meta:
        model = ImageProduct
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ReviewSerializer(serializers.ModelSerializer):

    """Сериализатор отзывов к товару"""

    class Meta:
        model = Review
        fields = [
            "author",
            "email",
            "text",
            "rate",
            "date",
        ]


class TagSerializer(serializers.ModelSerializer):

    """Сериализатор тегов"""

    class Meta:
        model = Tag
        fields = ["id", "name"]


class SpecificationsSerializer(serializers.ModelSerializer):

    """Сериализатор характеристик товара"""

    class Meta:
        model = Specification
        fields = ["name", "value"]


class ProductSerializer(serializers.ModelSerializer):

    """Сериализатор товаров"""

    category = CategorySerializer()
    images = ImageProductSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationsSerializer(many=True)
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
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]

    def get_rating(self, obj):
        return obj.avg_rating


class CatalogSerializer(serializers.ModelSerializer):

    """Сериализато каталога товаров"""

    category = CategorySerializer()
    images = ImageProductSerializer(many=True)
    tags = TagSerializer(many=True)
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

    def get_rating(self, obj):
        return obj.avg_rating


class SaleSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source="product.id", read_only=True)
    price = serializers.DecimalField(
        source="product.price", decimal_places=2, max_digits=10
    )
    salePrice = serializers.IntegerField()
    dateFrom = serializers.DateField()
    dateTo = serializers.DateField()
    title = serializers.CharField(source="product.title")
    images = ImageProductSerializer(source="product.images", many=True)

    class Meta:
        model = Sale
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]
