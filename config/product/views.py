from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

def add_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if not request.user.is_authenticated:
        return redirect("login")  # or your login URL name

    cart = get_or_create_cart(request.user)
    add_to_cart(cart, product)

    return redirect("cart")

class CartView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["cart"] = Cart.objects.filter(
                user=self.request.user
            ).first()
        else:
            context["cart"] = None

        return context
    
    @login_required
    def add_to_cart(request, product_id):
        product = get_object_or_404(Product, id=product_id)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

        if not created:
            cart_item.quantity += 1

        cart_item.save()
        return redirect('cart')
    
    class CartView(TemplateView):
        template_name = 'cart/cart.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            context['cart'] = cart
            return context
        
        @login_required
        def remove_from_cart(request, item_id):
            item = get_object_or_404(CartItem, id=item_id)
            item.delete()
            return redirect('cart') 
        
        def reduce_stock(product: Product, quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    if product.count < quantity:
        raise ValueError("Insufficient stock")

    product.count -= quantity
    product.save(update_fields=["count"])
