# Generated by Django 4.2.2 on 2023-06-08 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_reviewrating_user_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='user_picture',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
