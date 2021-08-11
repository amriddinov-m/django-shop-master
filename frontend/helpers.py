from product.models import Product


def calculate_cart(cart):
    products = Product.objects.filter(id__in=cart.keys())
    total = 0
    for product in products:
        total += (product.price * cart[str(product.id)])
    return total


def calculate_count_cart(cart):
    total = 0
    for v in cart.values():
        total += int(v)
    return total
