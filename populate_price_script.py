import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from product.models import Product
import random


def populate_price():
    # Get all products
    products = Product.objects.all()

    # Loop through each product
    for product in products:
        # first delete existing price
        product.price = 0
        # if product category is sticker, set price to [39,49,29] randomly
        if str(product.category) == "stickers":
            product.price = random.choice([39, 49, 29])
        if str(product.category) == "keychains":
            product.price = random.choice([9, 19, 29])
        if str(product.category) == "arts":
            product.price = random.choice([99, 79, 129])
        if str(product.category) == "figurines":
            product.price = random.choice([599, 699, 549])
        if str(product.category) == "acrylics":
            product.price = random.choice([399, 349, 299])
        if str(product.category) == "plushies":
            product.price = random.choice([199, 299, 249])

        # save the product
        product.save()

populate_price()