# Generated by Django 4.2.2 on 2023-06-08 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='static/images/categories'),
        ),
    ]