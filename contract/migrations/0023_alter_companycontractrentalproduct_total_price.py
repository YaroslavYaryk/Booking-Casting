# Generated by Django 4.0.4 on 2022-07-03 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0022_alter_companycontractrentalproduct_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companycontractrentalproduct',
            name='total_price',
            field=models.FloatField(default=0, null=True, verbose_name='Total product price'),
        ),
    ]
