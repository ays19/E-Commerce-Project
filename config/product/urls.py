from django.urls import path

from .views import (
    Home,
    ProductDetails,
    CartView,
    add_to_cart,
    remove_from_cart,
    checkout,
    order_success,
    payment_success,
    MyOrdersView,
    OrderDetailView,
    cancel_order,
)

app_name = "product"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("product/<slug:slug>/", ProductDetails.as_view(), name="product_detail"),

    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),

    path("checkout/", checkout, name="checkout"),
    path("order/success/", order_success, name="order_success"),
    path("payment/success/<int:order_id>/", payment_success, name="payment_success"),

    path("orders/", MyOrdersView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),

    path("orders/<int:pk>/cancel/", cancel_order, name="cancel_order"),
]
