from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='products_images/', null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def is_in_stock(self):
        return self.stock > 0
