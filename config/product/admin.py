from django.contrib import admin
from .models import Category, Product, Slider

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