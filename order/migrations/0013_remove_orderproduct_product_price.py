# Generated by Django 4.1 on 2023-05-21 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_rename_gift_charge_order_gift_charges'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='product_price',
        ),
    ]
