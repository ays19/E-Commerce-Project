from django.urls import path
from .views import (Home, ProductDetails, CartView, add_to_cart, checkout, remove_from_cart, order_success,
                    )

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('product/<slug:slug>/', ProductDetails.as_view(), name='product-details'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='cart_remove'),
    path("order-success/", order_success, name="order_success"),
    path("checkout/", checkout, name="checkout"),
    path("order-success/", order_success, name="order_success"),

]