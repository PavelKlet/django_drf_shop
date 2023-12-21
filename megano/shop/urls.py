from django.urls import path
from .views import (
    CategoryListAPIView,
    ProductRetrieveAPIView,
    ReviewAPIView,
    TagListAPIView,
    CatalogAPIView,
    PopularListAPIView,
    LimitedListAPIView,
    BannersListAPIView,
    SalesAPIView,
)

appname = "shop"

urlpatterns = [
    path("categories", CategoryListAPIView.as_view(), name="category"),
    path("product/<int:pk>", ProductRetrieveAPIView.as_view(), name="product"),
    path("product/<int:pk>/reviews", ReviewAPIView.as_view(), name="review"),
    path("tags", TagListAPIView.as_view(), name="tags"),
    path("catalog", CatalogAPIView.as_view(), name="catalog"),
    path("products/popular", PopularListAPIView.as_view(), name="popular"),
    path("products/limited", LimitedListAPIView.as_view(), name="limited"),
    path("banners", BannersListAPIView.as_view(), name="banners"),
    path("sales", SalesAPIView.as_view(), name="sales"),
]
