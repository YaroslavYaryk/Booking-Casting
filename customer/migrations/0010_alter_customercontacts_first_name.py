# Generated by Django 4.0.4 on 2022-05-24 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_alter_customeraccess_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customercontacts',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='first name'),
        ),
    ]
