from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .models import (
    Product,
    Slider,
    Category,
    Cart,
    CartItem,
    Order,
    OrderItem,
)

# Utility: Reduce Stock Safely
def reduce_stock(product: Product, quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    if product.count < quantity:
        raise ValueError(f"Insufficient stock for {product.title}")

    product.count -= quantity
    product.save(update_fields=["count"])


# Home Page
class Home(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(count__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sliders"] = Slider.objects.filter(show=True)
        context["categories"] = Category.objects.all()
        return context


# Product Details Page
class ProductDetails(DetailView):
    model = Product
    template_name = "product/product-details.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Related products (same category)
        context["related_products"] = Product.objects.filter(
            category=product.category,
            count__gt=0
        ).exclude(id=product.id)[:4]

        return context

# Cart View
class CartView(TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            context["cart"] = cart
            context["has_items"] = cart.items.exists()
        else:
            context["cart"] = None
            context["has_items"] = False

        return context
    
# Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.count <= 0:
        messages.error(request, "Product is out of stock")
        return redirect("product-details", slug=product.slug)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )

    if not created:
        if cart_item.quantity + 1 > product.count:
            messages.error(request, "Not enough stock available")
            return redirect("cart")
        cart_item.quantity += 1

    cart_item.save()
    messages.success(request, "Product added to cart")
    return redirect("cart")


# Remove from Cart
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )
    item.delete()
    messages.success(request, "Item removed from cart")
    return redirect("cart")

#Checkout
@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty")
        return redirect("cart")

    total = sum(
        item.product.price * item.quantity
        for item in cart.items.all()
    )

    if request.method == "POST":
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    email=request.POST.get("email"),
                    phone=request.POST.get("phone"),
                    address=request.POST.get("address"),
                    total_amount=total,
                )

                for item in cart.items.all():
                    if item.product.count < item.quantity:
                        raise ValueError(
                            f"Insufficient stock for {item.product.title}"
                        )

                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.price,
                        quantity=item.quantity,
                    )

                    item.product.count -= item.quantity
                    item.product.save(update_fields=["count"])

                cart.items.all().delete()

            messages.success(request, "Order placed successfully!")
            return redirect("order_success")

        except Exception as e:
            messages.error(request, str(e))
            return redirect("checkout")

    return render(
        request,
        "order/checkout.html",
        {
            "cart": cart,
            "cart_total": total,
        }
    )

# Order Success
@login_required
def order_success(request):
    return render(request, "order/success.html")
