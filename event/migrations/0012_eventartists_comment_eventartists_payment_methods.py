# Generated by Django 4.0.4 on 2022-05-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_alter_eventartists_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventartists',
            name='comment',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Comment'),
        ),
        migrations.AddField(
            model_name='eventartists',
            name='payment_methods',
            field=models.CharField(max_length=100, null=True, verbose_name='Payment Methods'),
        ),
    ]
