# Generated by Django 4.0.4 on 2022-07-09 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0004_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_brifing',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
