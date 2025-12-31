from django.db import models

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
    price= models.DecimalField(max_digits=9, decimal_places=2)
    description= models.TextField(null=True, blank=True, default='N/A')
    created_date= models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(auto_now=True)
    thumbnail= models.URLField()

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

