# Generated by Django 4.2.2 on 2023-06-09 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_avg_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_reviews',
            field=models.IntegerField(default=0),
        ),
    ]
