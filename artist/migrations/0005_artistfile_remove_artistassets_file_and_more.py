# Generated by Django 4.0.4 on 2022-05-05 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0004_artistrequestsstorage_done_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='artist_assets')),
            ],
        ),
        migrations.RemoveField(
            model_name='artistassets',
            name='file',
        ),
        migrations.AddField(
            model_name='artistassets',
            name='file',
            field=models.ManyToManyField(to='artist.artistfile'),
        ),
    ]
