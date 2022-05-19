# Generated by Django 4.0.4 on 2022-05-19 11:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0013_alter_artistaccess_unique_together_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0007_alter_event_contract_template'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventartists',
            unique_together={('event', 'artist')},
        ),
        migrations.AlterUniqueTogether(
            name='eventrentalproducts',
            unique_together={('event', 'rental_products')},
        ),
        migrations.AlterUniqueTogether(
            name='eventteam',
            unique_together={('event', 'user')},
        ),
    ]
