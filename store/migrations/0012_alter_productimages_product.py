# Generated by Django 5.0.2 on 2024-04-07 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_orderitem_order_productimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimages',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.product'),
        ),
    ]