# Generated by Django 4.0.4 on 2022-06-07 10:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contract', '0012_contractrentalproducts_timeclock_contracttimeclock_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contracteventrentalproducts',
            old_name='event',
            new_name='contract',
        ),
        migrations.RenameField(
            model_name='contracteventteam',
            old_name='event',
            new_name='contract',
        ),
        migrations.AlterUniqueTogether(
            name='contracteventrentalproducts',
            unique_together={('contract', 'rental_products')},
        ),
        migrations.AlterUniqueTogether(
            name='contracteventteam',
            unique_together={('contract', 'user')},
        ),
    ]
