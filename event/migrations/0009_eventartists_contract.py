# Generated by Django 4.0.4 on 2022-05-23 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_alter_eventartists_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventartists',
            name='contract',
            field=models.FileField(null=True, upload_to='artist_contract/', verbose_name='Artist Contract'),
        ),
    ]
