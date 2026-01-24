from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_GET

from .models import (
    Product,
    Slider,
    Category,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


# -------- Utilities --------
def reduce_stock(product: Product, quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    if product.count < quantity:
        raise ValueError(f"Insufficient stock for {product.title}")

    product.count -= quantity
    product.save(update_fields=["count"])


# -------- Pages --------
class Home(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(count__gt=0).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sliders"] = Slider.objects.filter(show=True)
        context["categories"] = Category.objects.all()
        return context


class ProductDetails(DetailView):
    model = Product
    template_name = "product/product-details.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context["related_products"] = (
            Product.objects.filter(category=product.category, count__gt=0)
            .exclude(id=product.id)[:4]
        )
        return context


# -------- Cart --------
class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context["cart"] = cart
        context["has_items"] = cart.items.exists()
        return context


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.count <= 0:
        messages.error(request, "Product is out of stock")
        # ✅ url name must match urls.py (if you use product_detail)
        return redirect("product_detail", slug=product.slug)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": 1},
    )

    if not created:
        if cart_item.quantity + 1 > product.count:
            messages.error(request, "Not enough stock available")
            return redirect("cart")
        cart_item.quantity += 1
        cart_item.save(update_fields=["quantity"])

    messages.success(request, "Product added to cart")
    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart")
    return redirect("cart")


# -------- Checkout & Payment --------
@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty")
        return redirect("cart")

    cart_total = sum(item.product.price * item.quantity for item in cart.items.all())

    if request.method == "POST":
        try:
            with transaction.atomic():
                payment_method = request.POST.get("payment_method", "cod")

                order = Order.objects.create(
                    user=request.user,
                    first_name=request.POST.get("first_name", "").strip(),
                    last_name=request.POST.get("last_name", "").strip(),
                    email=request.POST.get("email", "").strip(),
                    phone=request.POST.get("phone", "").strip(),
                    address=request.POST.get("address", "").strip(),
                    total_amount=cart_total,
                    payment_method=payment_method,
                )

                # Paid methods (mock) -> paid + processing
                if payment_method in ["card", "bkash"]:
                    order.is_paid = True
                    order.status = "processing"
                    order.save(update_fields=["is_paid", "status"])

                # Create order items + reduce stock
                for item in cart.items.select_related("product"):
                    reduce_stock(item.product, item.quantity)

                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.price,
                        quantity=item.quantity,
                    )

                # Clear cart
                cart.items.all().delete()

            messages.success(request, "Order placed successfully!")

            # ✅ redirect based on payment status
            if order.is_paid:
                return redirect("payment_success", order_id=order.id)

            return redirect("order_success")

        except Exception as e:
            messages.error(request, str(e))
            return redirect("checkout")

    return render(
        request,
        "order/checkout.html",
        {"cart": cart, "cart_total": cart_total},
    )


@login_required
def order_success(request):
    return render(request, "order/success.html")


@login_required
@require_GET
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order/payment_success.html", {"order": order})


# -------- Orders (User) --------
class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order/orders.html"
    context_object_name = "orders"
    login_url = "login"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "order/order_detail.html"
    context_object_name = "order"
    login_url = "login"

    def get_queryset(self):
        # Security: user can only see their own orders
        return Order.objects.filter(user=self.request.user)

@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if order.status != "pending":
        messages.error(request, "You cannot cancel this order")
        return redirect("product:order_detail", pk=pk)

    order.status = "cancelled"
    order.save(update_fields=["status"])

    messages.success(request, "Order cancelled successfully")
    return redirect("product:orders")