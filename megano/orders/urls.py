from django.urls import path
from .views import CartAPIView, OrdersAPIView, OrderAPIView, PaymentAPIView

appname = "orders"

urlpatterns = [
    path("basket", CartAPIView.as_view(), name="basket"),
    path("orders", OrdersAPIView.as_view(), name="orders"),
    path("order/<int:order_id>", OrderAPIView.as_view(), name="order"),
    path("payment/<int:order_id>", PaymentAPIView.as_view(), name="payment"),
]
