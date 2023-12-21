from django.contrib import admin

from .forms import SaleDateForm
from .models import (
    Category,
    ImageCategory,
    Product,
    ImageProduct,
    Tag,
    Review,
    Specification,
    Sale,
)


class ImageCategoryInline(admin.TabularInline):
    model = ImageCategory
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pk",
        "parent_category",
    )
    list_filter = ("parent_category",)
    search_fields = ("title",)

    def delete_selected(self, request, queryset):
        queryset.delete()

    actions = [delete_selected]
    inlines = [ImageCategoryInline]


class ImageProductInline(admin.TabularInline):
    model = ImageProduct
    extra = 3


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    class Meta:
        model = Specification
        list_display = ("name", "value")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


class TagInline(admin.TabularInline):
    model = Tag.product.through


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "email", "text", "rate", "product")


class SpecificationInline(admin.TabularInline):
    model = Specification


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "price",
        "count",
        "date",
        "title",
        "short_description",
        "freeDelivery",
        "short_full_description",
        "limited",
    )
    list_display_links = ("title",)
    inlines = [ImageProductInline, TagInline, SpecificationInline]

    def short_description(self, obj):
        return obj.description[:100] if obj.description else ""

    def short_full_description(self, obj):
        return obj.fullDescription[:250] if obj.fullDescription else ""


@admin.register(Sale)
class SalesAdmin(admin.ModelAdmin):
    list_display = ("product_title", "salePrice", "dateFrom", "dateTo")
    form = SaleDateForm

    def product_title(self, obj):
        return obj.product.title
