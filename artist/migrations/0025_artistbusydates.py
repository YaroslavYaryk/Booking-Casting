# Generated by Django 4.0.4 on 2022-06-24 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0024_alter_artist_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistBusyDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='start_date')),
                ('end_date', models.DateField(verbose_name='end_date')),
                ('busy_action', models.CharField(max_length=200)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artist.artist', verbose_name='Artist')),
            ],
        ),
    ]