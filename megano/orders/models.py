from django.db import models

from accounts.models import Profile
from shop.models import Product


class Order(models.Model):
    profile = models.ForeignKey(
        Profile, related_name="orders", verbose_name="Заказы", on_delete=models.CASCADE
    )
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Создано в дату")
    fullName = models.CharField(blank=True, null=True, max_length=128)
    email = models.EmailField(max_length=100)
    phone = models.CharField(
        blank=True, null=True, verbose_name="Номер телефона", max_length=12
    )
    DELIVERY_CHOICES = [
        ("express", "Express Delivery"),
        ("ordinary", "Ordinary Delivery"),
        ("standard", "Standard Delivery"),
    ]
    deliveryType = models.CharField(
        max_length=20, choices=DELIVERY_CHOICES, default="standard"
    )
    PAYMENT_CHOICES = [("online", "Online Payment"), ("someone", "Someone payment")]
    paymentType = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default="online"
    )
    totalCost = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True
    )
    status = models.CharField(max_length=20, default="accepted")
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    products = models.ManyToManyField(
        Product, through="OrderItem", related_name="orders", verbose_name="Продукты"
    )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1)
