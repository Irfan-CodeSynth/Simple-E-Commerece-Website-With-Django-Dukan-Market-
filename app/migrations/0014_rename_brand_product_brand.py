# Generated by Django 5.0.7 on 2024-07-27 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_brand_product_brand'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='brand',
            new_name='Brand',
        ),
    ]
