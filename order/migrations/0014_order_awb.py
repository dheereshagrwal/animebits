# Generated by Django 4.1 on 2023-05-21 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_remove_orderproduct_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='awb',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]