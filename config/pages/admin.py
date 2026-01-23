from django.contrib import admin
from .models import Category, Product, Slider, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "created_date")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
    list_filter = ("featured",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "count", "featured", "created_date")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "category__title")
    list_filter = ("category", "featured")
    list_editable = ("price", "count", "featured")
    ordering = ("-id",)

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "show", "created_date")
    list_filter = ("show",)
    search_fields = ("title",)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price", "quantity")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "payment_method", "status", "is_paid", "created_at")
    list_filter = ("status", "is_paid", "payment_method", "created_at")
    search_fields = ("id", "user__username", "email", "phone")
    inlines = [OrderItemInline]
    readonly_fields = ("total_amount", "created_at")

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("created_at",)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")
    search_fields = ("product__title",)