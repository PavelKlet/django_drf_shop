from django.conf import settings
from shop.models import Product


class Cart(object):
    """Класс управления корзиной"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": quantity}
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, quantity, product):
        product_id = str(product.id)
        if product_id in self.cart:
            amount_received = self.cart[product_id]["quantity"] - quantity
            if amount_received <= 0:
                del self.cart[product_id]
                if not self.cart:
                    self.clear()
            else:
                self.cart[product_id]["quantity"] -= quantity
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def receive(self):
        product_ids = [int(product_id) for product_id in self.cart.keys()]
        return Product.objects.filter(id__in=product_ids)

    def get_quantity(self, product):
        product_id = str(product.id)
        return self.cart[product_id]["quantity"]

    def empty(self):
        return True if not self.cart else False
