from django.contrib import admin
from .models import Category, Product, Slider,Order, OrderItem

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "featured", "created_date")
    search_fields = ("title",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "price", "count", "featured")
    list_filter = ("featured", "category")
    search_fields = ("title",)

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
    list_display = ("id", "user", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "email", "phone")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]