from django.core.validators import MinValueValidator
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default = 5,
    )


    def __str__(self):
        return f"Review for {self.product.title}"

