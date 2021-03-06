# Generated by Django 4.0.4 on 2022-05-08 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0008_artist_owner_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistaccess',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artist.artist', unique=True, verbose_name='artist_access'),
        ),
    ]
