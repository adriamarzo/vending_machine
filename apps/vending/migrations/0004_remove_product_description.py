# Generated by Django 4.2.2 on 2023-09-01 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vending', '0003_vendingmachineslot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
    ]
