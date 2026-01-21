from django.urls import path
from .views import (
    Home,
    ProductDetails,
    CartView,
    add_to_cart,
    my_orders,
    order_detail,
    remove_from_cart,
    checkout,
    order_success,
    MyOrdersView, OrderDetailView
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("product/<slug:slug>/", ProductDetails.as_view(), name="product-details"),
    path("cart/", CartView.as_view(), name="cart"),
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:item_id>/", remove_from_cart, name="cart_remove"),
    path("checkout/", checkout, name="checkout"),
    path("order-success/", order_success, name="order_success"),
    path("orders/", MyOrdersView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("my-orders/", my_orders, name="my_orders"),
    path("orders/<int:pk>/", order_detail, name="order_detail"),


]
