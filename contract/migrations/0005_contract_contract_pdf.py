# Generated by Django 4.0.4 on 2022-05-29 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0004_alter_contract_payment_methods'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='contract_pdf',
            field=models.CharField(max_length=150, null=True, verbose_name='Contract PDF'),
        ),
    ]