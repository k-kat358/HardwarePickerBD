# Generated by Django 5.1.2 on 2025-04-01 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_case_product_type_alter_cpucooler_product_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobo',
            name='product_type',
            field=models.CharField(default='mobo', max_length=20),
        ),
    ]
