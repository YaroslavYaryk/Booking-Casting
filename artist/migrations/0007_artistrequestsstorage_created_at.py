# Generated by Django 4.0.4 on 2022-05-06 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0006_artistfile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistrequestsstorage',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
