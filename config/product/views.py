from django.views.generic import ListView, DetailView
from .models import Product, Slider, Category
from django.shortcuts import redirect, get_object_or_404
from product.services import get_or_create_cart, add_to_cart


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

