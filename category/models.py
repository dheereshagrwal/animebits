from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(max_length=25, unique=True)
    image = models.ImageField(upload_to="static/images/categories")

    class Meta:
        verbose_name_plural = "Categories"

    def get_url(self):
        return reverse("products_by_category", args=[self.slug])

    def __str__(self):
        return self.name
