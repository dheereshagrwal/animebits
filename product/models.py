from django.db import models
from category.models import Category
from django.urls import reverse
from django.core.validators import MinValueValidator


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField(default=99)
    stock = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to="images/products")
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("product_details", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name



class VariationManager(models.Manager):
    def gifts(self):
        return super(VariationManager, self).filter(variation_category="gift", is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category="size", is_active=True)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=50,
        choices=(("size", "size"), ("gift", "gift")),
        default="size",
    )
    variation_value = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    objects = VariationManager()
    def __str__(self):
        return self.variation_value
