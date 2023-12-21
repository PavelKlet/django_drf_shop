from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


def path_category_image(instance: "ImageCategory", filename: str) -> str:
    """Функция генерации уникального пути к изображению категории"""

    return f"category/{instance.alt}/{filename}"


def path_products_image(instance: "ImageCategory", filename: str) -> str:
    """Функция генерации уникального пути к изображению товара"""

    return f"products/{instance.alt}/{filename}"


class Category(models.Model):

    """Модель категорий товаров"""

    title = models.CharField(max_length=125)
    parent_category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subcategories",
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        if self.parent_category:
            return f"{self.parent_category.title} {self.title}"
        return self.title


class ImageCategory(models.Model):

    """Модель изображения категории"""

    src = models.ImageField(
        upload_to=path_category_image,
        verbose_name="Изображение категории",
    )
    alt = models.CharField(
        max_length=123, verbose_name="Описание изображения категории"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="image",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name_plural = "Images categories"

    def __str__(self):
        return self.alt


class Review(models.Model):

    """Модель отзыва к товару"""

    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=125, verbose_name="Email address")
    text = models.CharField(max_length=2500)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="reviews"
    )


class Product(models.Model):

    """Модель товаров"""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product"
    )
    price = models.DecimalField(max_digits=20, decimal_places=2)
    count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=125)
    description = models.CharField(max_length=1000)
    fullDescription = models.CharField(max_length=2500, null=True, blank=True)
    freeDelivery = models.BooleanField(default=False, verbose_name="Free delivery")
    available = models.BooleanField(default=True, verbose_name="Available")
    limited = models.BooleanField(default=False, verbose_name="Limited")

    @property
    def avg_rating(self):
        return self.reviews.aggregate(avg_rating=Avg("rate")).get("avg_rating", 0)

    def __str__(self):
        return self.title


class ImageProduct(models.Model):

    """Модель изображений товаров"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    src = models.ImageField(
        upload_to=path_products_image, verbose_name="Изображения продукта"
    )
    alt = models.CharField(max_length=125, verbose_name="Описание изображения продукта")


class Tag(models.Model):

    """Модель тегов"""

    name = models.CharField(max_length=33)
    product = models.ManyToManyField(Product, related_name="tags")

    def __str__(self):
        return self.name


class Specification(models.Model):

    """Модель технических характеристик"""

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=2500)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications"
    )

    def __str__(self):
        return self.name


class Sale(models.Model):

    """Модель распродажи товаров"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    salePrice = models.DecimalField(
        decimal_places=2,
        max_digits=10,
    )
    dateFrom = models.DateField()
    dateTo = models.DateField()
