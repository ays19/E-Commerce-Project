from django.db import models
from django.conf import settings

class Category(models.Model):
    title= models.CharField(max_length=150, unique=True)
    slug= models.SlugField(unique=True)
    featured= models.BooleanField(default=False)
    created_date= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering= ['title']

    def __str__(self) -> str:
        return self.title
    
class Product(models.Model):
    category= models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title= models.CharField(max_length=150, unique=True)
    slug= models.SlugField(unique=True)
    featured= models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    description= models.TextField(null=True, blank=True, default='N/A')
    created_date= models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(auto_now=True)
    thumbnail= models.URLField()

class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)    

    class Meta:
        ordering= ['-id']

    def __str__(self) -> str:
        return self.title
    
class Slider(models.Model):
    title= models.CharField(max_length=150, unique=True)
    banner= models.ImageField(upload_to='banners')
    show= models.BooleanField(default=True)
    created_date= models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

