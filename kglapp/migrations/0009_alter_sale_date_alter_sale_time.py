# Generated by Django 4.2.20 on 2025-03-27 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kglapp', '0008_delete_record_credit_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
