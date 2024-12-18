import json
from . models import *


def cookieCart(request):
 try:
      cart = json.loads(request.COOKIES.get('cart', '{}'))
 except json.JSONDecodeError:
            cart = {}
 items = []
 order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
 cartItems = 0

 for i in cart:
            try:
                cartItems += cart[i]["quantity"]

                product = Product.objects.get(id=i)
                total = product.price * cart[i]["quantity"]

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]["quantity"]

                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]["quantity"],
                    'get_total': total,
                }
                items.append(item)
            except Product.DoesNotExist:
                # Handle missing product gracefully
                continue
 return {'cartItems':cartItems, 'order': order, 'items': items}