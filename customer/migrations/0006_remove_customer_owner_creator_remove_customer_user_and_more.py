# Generated by Django 4.0.4 on 2022-05-10 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0005_customeraccess'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='owner_creator',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='customeraccess',
            name='access',
        ),
        migrations.AddField(
            model_name='customeraccess',
            name='access',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='access'),
        ),
    ]
