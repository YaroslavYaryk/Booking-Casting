# Generated by Django 4.0.4 on 2022-05-13 13:32

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='contract',
            field=ckeditor.fields.RichTextField(verbose_name='Contract'),
        ),
    ]
