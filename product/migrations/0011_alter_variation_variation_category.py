# Generated by Django 4.1 on 2023-05-15 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_alter_variation_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(blank=True, choices=[('size', 'size'), ('gift', 'gift')], default='size', max_length=50, null=True),
        ),
    ]
