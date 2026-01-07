from product.models import Product
from product.models import Cart, CartItem


def reduce_stock(product: Product, quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    if product.count < quantity:
        raise ValueError("Insufficient stock")

    product.count -= quantity
    product.save(update_fields=["count"])

def get_or_create_cart(user):
    """
    Returns existing cart or creates a new one for the user
    """
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def add_to_cart(cart, product, quantity=1):
    """
    Adds product to cart safely
    """
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if item.quantity + quantity > product.count:
        raise ValueError("Not enough stock available")

    item.quantity += quantity
    item.save()