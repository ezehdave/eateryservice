# Generated by Django 4.0.4 on 2022-09-02 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0010_remove_delivery_order_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.OneToOneField(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='storeapp.producttype'),
        ),
    ]
