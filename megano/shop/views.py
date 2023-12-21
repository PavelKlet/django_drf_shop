from rest_framework.views import APIView, Request, Response
from rest_framework.generics import get_object_or_404, ListAPIView, RetrieveAPIView
from rest_framework import status
from django.db.models import Count

from .models import Category, Product, Tag, Sale
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    TagSerializer,
    CatalogSerializer,
)
from .paginations import CatalogPaginator, SalePaginator
from .filters import CatalogFilter


class CategoryListAPIView(ListAPIView):

    """Представление категорий товаров"""

    queryset = Category.objects.filter(parent_category_id__isnull=True)
    serializer_class = CategorySerializer


class ProductRetrieveAPIView(RetrieveAPIView):

    """Представление товара"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewAPIView(APIView):

    """Представление создания отзывов к товару"""

    def post(self, request: Request, pk) -> Response:
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(Product, pk=pk)
            serializer.save(product=product)
            return Response("Отзыв успешно создан", status=status.HTTP_200_OK)
        return Response(
            "Ошибка при создании отзыва", status=status.HTTP_400_BAD_REQUEST
        )


class TagListAPIView(ListAPIView):

    """Представление тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CatalogAPIView(APIView):

    """Представление каталога товаров"""

    def get(self, request: Request) -> Response:
        get_params = request.GET.items()
        filter_params = {}
        for name, value in get_params:
            if name.startswith("filter["):
                field_name = name.split("[")[1].split("]")[0].strip()
                filter_params[field_name] = value
            else:
                filter_params[name] = value

        filter_instance = CatalogFilter(filter_params, queryset=Product.objects.all())

        if not filter_instance.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=filter_instance.errors
            )

        sort = request.GET.get("sort")
        filtered_queryset = filter_instance.qs.order_by(sort)
        limit = request.GET.get("limit")
        paginator = CatalogPaginator(filtered_queryset, int(limit))
        page_number = request.GET.get("currentPage")
        paginated_data = paginator.get_paginated_data(int(page_number))
        return Response(paginated_data)


class PopularListAPIView(ListAPIView):

    """Представление популярных товаров"""

    queryset = (
        Product.objects.filter(limited=False)
        .annotate(num_reviews=Count("reviews"))
        .order_by("-num_reviews")[:8]
    )
    serializer_class = CatalogSerializer


class LimitedListAPIView(ListAPIView):

    """Представление лимитированных товаров"""

    queryset = Product.objects.filter(limited=True)
    serializer_class = CatalogSerializer


class BannersListAPIView(ListAPIView):

    """Представление баннеров"""

    queryset = Product.objects.all().order_by("?")[:3]
    serializer_class = CatalogSerializer


class SalesAPIView(APIView):

    """Представление распродажи товаров"""

    def get(self, request):
        queryset = Sale.objects.all()
        current_page = request.GET.get("currentPage")
        paginator = SalePaginator(queryset, 10)
        paginated_data = paginator.get_paginated_data(current_page)
        return Response(paginated_data)
