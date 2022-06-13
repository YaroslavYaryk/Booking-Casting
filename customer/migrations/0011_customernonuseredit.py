# Generated by Django 4.0.4 on 2022-06-10 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_alter_customercontacts_first_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerNonUserEdit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=100, verbose_name='User Email')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer', verbose_name='Customer')),
            ],
            options={
                'unique_together': {('customer', 'user_email')},
            },
        ),
    ]
