# Generated by Django 4.0.4 on 2022-05-05 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0005_artistfile_remove_artistassets_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistfile',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
    ]
