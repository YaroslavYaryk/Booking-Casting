# Generated by Django 4.0.4 on 2022-05-06 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_customer_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='zip_code',
            field=models.CharField(max_length=255, verbose_name='Zip Code'),
        ),
    ]
