# Generated by Django 3.2.19 on 2023-06-06 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrating',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_ratings', to='products.product'),
        ),
    ]
