from django.core.management.base import BaseCommand
from product.models import Category, Product
from django.utils.text import slugify
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Adding producrt...")
        url = "https://fakestoreapi.com/products"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            self.stderr.write("Failed to fetch data from API")
            return
        products = response.json()
        
        for product in products:
            category, _ = Category.objects.get_or_create(
                title=product['category'],
                slug=slugify(product['category']),
                featured=True
            )
            Product.objects.create(
                category= category,
                title= product['title'],
                slug= slugify(product['title']),
                price= product['price'],
                thumbnail= product['image'],
                description= product['description']
            # rate =Product['rating']['rate'],
            # count =Product['rating']['count']
        )

        print("Products added successfully")