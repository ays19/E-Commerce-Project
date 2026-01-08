from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import (Product,Slider,Category,Cart,CartItem,Order,OrderItem,)

def reduce_stock(product: Product, quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    if product.count < quantity:
        raise ValueError("Insufficient stock")

    product.count -= quantity
    product.save(update_fields=["count"])

class Home(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(featured=True, count__gt=0)

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

class CartView(TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            context["cart"] = cart
        else:
            context["cart"] = None
        return context
    
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    messages.success(request, "Product added to cart")
    return redirect('cart')
    
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart")
    return redirect("cart")

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
                        raise ValueError("Insufficient stock")
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.price,
                        quantity=item.quantity,
                    )
                    # reduce stock
                    item.product.count -= item.quantity
                    item.product.save()

                     # clear cart
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
            "cart_total": total
        }
    )

