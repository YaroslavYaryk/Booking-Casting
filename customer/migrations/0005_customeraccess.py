# Generated by Django 4.0.4 on 2022-05-09 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0004_customer_owner_creator_customerrequestsstorage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.BooleanField(default=False)),
                ('access', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customer.customer', verbose_name='customer_access')),
            ],
        ),
    ]
