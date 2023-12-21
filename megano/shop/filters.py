from django_filters import rest_framework as filters

from .models import Category, Product


class CatalogFilter(filters.FilterSet):

    """Фильтры каталога товаров"""

    maxPrice = filters.NumberFilter(field_name="price", lookup_expr="lte")
    minPrice = filters.NumberFilter(field_name="price", lookup_expr="gte")
    category = filters.NumberFilter(field_name="category__id", method="filter_category")
    name = filters.CharFilter(field_name="title", lookup_expr="icontains")
    freeDelivery = filters.BooleanFilter(field_name="freeDelivery")
    available = filters.BooleanFilter(field_name="available")

    class Meta:
        model = Product
        fields = ["price", "title", "freeDelivery", "available", "category"]

    def filter_category(self, queryset, name, value):
        if value is not None:
            category = Category.objects.get(id=value)
            if category.parent_category is None:
                child_categories = category.subcategories.all()
                category_ids = [
                    child_category.id for child_category in child_categories
                ]
                category_ids.append(category.id)
                queryset = queryset.filter(category__id__in=category_ids)
            else:
                queryset = queryset.filter(category__id=value)
            return queryset
