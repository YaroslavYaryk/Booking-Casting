# Generated by Django 4.0.4 on 2022-06-24 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0019_artist_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Date created'),
        ),
    ]
