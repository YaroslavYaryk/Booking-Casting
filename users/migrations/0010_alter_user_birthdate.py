# Generated by Django 4.0.4 on 2022-05-04 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_rename_abilitie_userabilities_ability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=models.DateField(blank=True),
        ),
    ]
