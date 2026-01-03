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
        
        for item in products:
            # Category (safe & reusable)
            category, _ = Category.objects.get_or_create(
                title=item.get("category", "Unknown"),
                slug=slugify(item.get("category", "unknown")),
                defaults={"featured": True},
            )

             # Unique slug handling
            slug = slugify(item.get("title", "product"))

            if Product.objects.filter(slug=slug).exists():
                continue  # prevent duplicates

            # Product creation (API-safe)
            Product.objects.create(
                category=category,
                title=item.get("title", "No title"),
                slug=slug,
                price=item.get("price", 0),
                count=item.get("rating", {}).get("count", 0),
                description=item.get("description", ""),
                thumbnail=item.get("image", ""),
            )

        self.stdout.write(
            self.style.SUCCESS("Products added successfully")
        )