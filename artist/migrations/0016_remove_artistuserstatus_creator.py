# Generated by Django 4.0.4 on 2022-06-02 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0015_artistuserstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artistuserstatus',
            name='creator',
        ),
    ]
