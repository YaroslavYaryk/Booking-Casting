# Generated by Django 4.0.4 on 2022-05-03 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
