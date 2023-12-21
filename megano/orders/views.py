import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from .serializers import CartProductsSerializer, OrderSerializer
from shop.models import Product
from .cart import Cart
from .models import Order, OrderItem


class CartAPIView(APIView):

    """Представление корзины товаров"""

    def post(self, request: Request) -> Response:
        product_id = request.data.get("id")
        quantity = request.data.get("count")
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, quantity)
        return Response(data=self.get_products(cart))

    def get(self, request):
        cart = Cart(request)
        if cart.empty():
            return Response(data={}, status=status.HTTP_200_OK)
        return Response(data=self.get_products(cart))

    def delete(self, request):
        cart = Cart(request)
        product_id = request.data.get("id")
        quantity = request.data.get("count")
        product = get_object_or_404(Product, id=product_id)
        cart.remove(quantity, product)
        if cart.empty():
            cart.clear()
            return Response(data={}, status=status.HTTP_200_OK)
        return Response(data=self.get_products(cart))

    def get_products(self, cart):
        products = cart.receive()
        serializer = CartProductsSerializer(products, many=True, context={"cart": cart})
        return serializer.data


class OrdersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        cart = Cart(request)
        if cart.empty():
            return Response(data="Пустая корзина", status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        product_ids = [item.get("id") for item in data]
        products = Product.objects.filter(id__in=product_ids)
        if not products:
            return Response(
                data="Продукты не найдены", status=status.HTTP_400_BAD_REQUEST
            )
        profile = request.user.profile
        order = Order.objects.create(profile=profile)
        for product in products:
            OrderItem.objects.create(
                order=order, product=product, quantity=cart.get_quantity(product)
            )
        return Response(data={"orderId": order.id}, status=status.HTTP_200_OK)

    def get(self, request: Request) -> Response:
        profile = request.user.profile
        serializer = OrderSerializer(profile.orders.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class OrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, order_id) -> Response:
        cart = Cart(request)
        if cart.empty():
            return Response(data="Пустая корзина", status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request: Request, order_id) -> Response:
        cart = Cart(request)
        if cart.empty():
            return Response(data="Пустая корзина", status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=order_id)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        serializer.save()
        cart.clear()

        return Response({"orderId": order_id}, status=status.HTTP_200_OK)


class PaymentAPIView(APIView):
    def post(self, request: Request, order_id) -> Response:
        return Response(status=status.HTTP_200_OK)
