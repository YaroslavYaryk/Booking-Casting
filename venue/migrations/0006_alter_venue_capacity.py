# Generated by Django 4.0.4 on 2022-05-13 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0005_alter_venue_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='capacity',
            field=models.CharField(max_length=255, verbose_name='Capacity'),
        ),
    ]
