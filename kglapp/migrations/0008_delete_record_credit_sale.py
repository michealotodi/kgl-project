# Generated by Django 4.2.20 on 2025-03-26 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kglapp', '0007_record_credit_sale_delete_sales'),
    ]

    operations = [
        migrations.DeleteModel(
            name='record_credit_sale',
        ),
    ]
