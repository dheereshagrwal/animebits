import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from product.models import Product, Variation

def populate_gift_variations():
    # Get all products
    products = Product.objects.all()

    # Loop through each product
    for product in products:
        # Delete existing gift variations for the current product
        Variation.objects.filter(product=product, variation_category='gift').delete()

        # Create new gift variations for the current product
        Variation.objects.create(product=product, variation_category='gift', variation_value='gift')
        Variation.objects.create(product=product, variation_category='gift', variation_value='no')

if __name__ == '__main__':
    populate_gift_variations()
