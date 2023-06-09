# Generated by Django 4.2.2 on 2023-06-08 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_productgallery_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='static/images/products'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='image',
            field=models.ImageField(max_length=255, upload_to='static/images/products'),
        ),
    ]
