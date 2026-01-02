from typing import Any
from django.core.management.base import BaseCommand
from config.product.models import Category, Product
import requests
from django.utils.text import slugify

class Command(BaseCommand):
    def handle(self, *args: **options):
    print("Adding producrt")
    response = requests.get('https://fakestoreapi.com/products').json()

    for product in response:
        category, _ = Category.objects.get_or_create(
            title=Product['category'],
            slug=slugify(Product['category']),
            featured=True
        )
        Product.objects.create(
            category=category,
            title=Product['title'],
            slug=slugify(Product['title']),
            price=Product['price'],
            thumbnail=Product['image'],
            description=Product['description'],
        )

    print("Products added successfully")