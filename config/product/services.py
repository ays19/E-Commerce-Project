from product.models import Product


def reduce_stock(product: Product, quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    if product.count < quantity:
        raise ValueError("Insufficient stock")

    product.count -= quantity
    product.save(update_fields=["count"])
