# Generated by Django 4.0.4 on 2022-05-13 13:50

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_event_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='contract',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
