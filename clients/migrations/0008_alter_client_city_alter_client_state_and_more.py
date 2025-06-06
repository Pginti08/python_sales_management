# Generated by Django 4.2.20 on 2025-04-28 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_alter_client_postal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.CharField(default=None, max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='state',
            field=models.CharField(default=None, max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='street_address',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
