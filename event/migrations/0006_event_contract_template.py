# Generated by Django 4.0.4 on 2022-05-15 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_remove_eventartists_artist_eventartists_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='contract_template',
            field=models.TextField(null=True),
        ),
    ]
